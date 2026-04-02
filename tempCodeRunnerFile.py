from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "r_global_key"

def get_db_connection():
    return psycopg2.connect(
        dbname="mohit_project", user="postgres",
        password="1234", host="localhost", port="5432"
    )

@app.route('/fix_db')
def fix_db():
    """Ensures all columns and tables for the cart and orders exist"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS image TEXT;")
        cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS rating INTEGER DEFAULT 5;")
        
        cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_amount DECIMAL(10,2);")
        cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS product_name TEXT;")
        cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'Pending';")
        cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id INTEGER;")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS "Cart" (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id),
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER,
                price DECIMAL(10,2)
            );
        """)
        
        conn.commit()
        return "Database synchronized: Columns and Cart table are ready!"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()

@app.route('/')
def dashboard_page():
    user_name = session.get('user', '')
    return render_template('m.html', user=user_name)

@app.route('/product')
def show_products():
    return render_template('Product.html', user=session.get('user', 'MOHIT'))

@app.route('/cart')
def cart_page():
    return render_template('cart.html', user=session.get('user', 'MOHIT'))

@app.route('/inventory')
def inventory_page():
    return render_template('inventory.html')

@app.route('/orders')
def order_page():
    return render_template('order.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s AND password = %s",
                    (data['username'], data['password']))
        user = cur.fetchone(); cur.close(); conn.close()

        if user:
            session['user'] = user[0]
            return jsonify({"status": "success", "redirect": "/"})
        return jsonify({"status": "error", "message": "Invalid Credentials"}), 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/get_menu')
def get_menu():
    menu_data = [
        {"name": "Dashboard", "route": "/", "": ""},
        {"name": "Order", "route": "/orders", "": ""},
        {"name": "Merchant", "route": "/", "": ""},
        {"name": "Inventory", "route": "/inventory", "": ""},
        {"name": "Product", "route": "/product", "": ""},
    ]
    return jsonify(menu_data)

@app.route('/get_products', methods=['GET'])
def get_products():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM products ORDER BY id DESC")
    products = cur.fetchall(); cur.close(); conn.close()
    return jsonify(products)

@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category = request.form.get('category')
        file = request.files.get('image_file')
        
        filename = secure_filename(file.filename) if file and file.filename != '' else 'default.jpg'
        if file and file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO products (name, price, stock, category, image)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, price, stock, category, filename))
        conn.commit(); cur.close(); conn.close()
        return jsonify({"status": "success", "message": "Product added"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"})

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    cart_items = data.get('items')
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    conn = get_db_connection(); cur = conn.cursor()
    try:
        total_bill = sum(float(item['price']) * int(item['quantity']) for item in cart_items)
        
        cur.execute("INSERT INTO orders (total_amount, status) VALUES (%s, 'Paid') RETURNING id", (total_bill,))
        new_order_id = cur.fetchone()[0]

        for item in cart_items:
            cur.execute("""
                INSERT INTO "Cart" (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (new_order_id, item['id'], item['quantity'], item['price']))
            
            cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s",
                        (item['quantity'], item['id']))

        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        cur.close(); conn.close()

@app.route('/get_orders')
def get_orders():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT o.id, COALESCE(u.username, 'Guest') as username, 
                   COALESCE(o.product_name, 'Multi-item Order') as product, 
                   o.total_amount, o.status, o.order_date as date
            FROM orders o 
            LEFT JOIN users u ON o.user_id = u.id 
            ORDER BY o.id DESC
        """)
        rows = cur.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close(); conn.close()

# --- Merchant & Seasons Logic ---
@app.route('/get_merchants', methods=['GET'])
def get_merchants():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM merchant_hierarchy ORDER BY id DESC")
    data = cur.fetchall(); cur.close(); conn.close()
    return jsonify(data)

@app.route('/get_seasons')
def get_seasons():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM seasons ORDER BY id DESC")
    data = cur.fetchall(); cur.close(); conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)