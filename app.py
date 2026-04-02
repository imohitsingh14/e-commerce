# from flask import Flask, render_template, jsonify, request, redirect, url_for, session 
# from werkzeug.utils import secure_filename
# import os
# import psycopg2 
# from psycopg2.extras import RealDictCursor

# app = Flask(__name__) 
# UPLOAD_FOLDER = 'static'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.secret_key = "r_global_key" 

# def get_db_connection(): 
#     return psycopg2.connect( 
#         dbname="mohit_project", user="postgres", 
#         password="1234", host="localhost", port="5432" 
#     ) 

# @app.route('/fix_db')
# def fix_db():
#     """Visit http://127.0.0.1:5000/fix_db to ensure columns exist"""
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS image TEXT;")
#         cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS rating INTEGER DEFAULT 5;")
#         conn.commit()
#         return "Database columns 'image' and 'rating' verified/added!"
#     except Exception as e:
#         return f"Error: {str(e)}"
#     finally:
#         cur.close()
#         conn.close()

# @app.route('/') 
# def dashboard_page(): 
#     user_name = session.get('user', 'MOHIT') 
#     return render_template('m.html', user=user_name)

# @app.route('/product')
# def show_products():
#     return render_template('Product.html')

# @app.route('/inventory')
# def inventory_page(): 
#     return render_template('inventory.html') 

# @app.route('/orders')
# def order_page():
#     return render_template('order.html')

# @app.route('/login', methods=['GET', 'POST']) 
# def login(): 
#     if request.method == 'POST':
#         data = request.json 
#         conn = get_db_connection(); cur = conn.cursor() 
#         cur.execute("SELECT username FROM users WHERE username = %s AND password = %s", 
#                     (data['username'], data['password'])) 
#         user = cur.fetchone(); cur.close(); conn.close() 

#         if user: 
#             session['user'] = user[0] 
#             return jsonify({"status": "success", "redirect": "/"}) 
#         return jsonify({"status": "error", "message": "Invalid Credentials"}), 401
#     return render_template('login.html')

# @app.route('/logout') 
# def logout(): 
#     session.pop('user', None) 
#     return redirect(url_for('login')) 


# @app.route('/get_menu')
# def get_menu():
#     menu_data = [
#         {"name": "Dashboard", "route": "/", "icon": ""},
#         {"name": "Order", "route": "/orders", "icon": ""},
#         {"name": "Merchant", "route": "/", "icon": ""},
#         {"name": "Inventory", "route": "/inventory", "icon": ""},
#         {"name": "Product", "route": "/product", "icon": ""},
#     ]
#     return jsonify(menu_data)

# @app.route('/get_products', methods=['GET'])
# def get_products():
#     conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT * FROM products ORDER BY id DESC")
#     products = cur.fetchall(); cur.close(); conn.close()
#     return jsonify(products)

# @app.route('/add_product', methods=['POST'])
# def add_product():
#     try:
#         name = request.form.get('name')
#         price = request.form.get('price')
#         stock = request.form.get('stock')
#         category = request.form.get('category')
#         file = request.files.get('image_file')
#         if file and file.filename != '':
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         else:
#             filename = 'default.jpg'
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO products (name, price, stock, category, image)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (name, price, stock, category, filename))
        
#         conn.commit()
#         cur.close()
#         conn.close()
#         return jsonify({"status": "success", "message": "Product added"}), 200

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500
    
# @app.route('/delete_product/<int:id>', methods=['DELETE'])
# def delete_product(id):
#     conn = get_db_connection(); cur = conn.cursor()
#     cur.execute("DELETE FROM products WHERE id = %s", (id,))
#     conn.commit(); cur.close(); conn.close()
#     return jsonify({"status": "success"})

# @app.route('/get_inventory')
# def get_inventory():
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#         cur.execute("SELECT id, name, category, price, stock, image, rating FROM products ORDER BY name ASC")
#         rows = cur.fetchall()
#         cur.close(); conn.close()
#         return jsonify(rows)
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route('/get_merchants', methods=['GET'])
# def get_merchants():
#     conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT * FROM merchant_hierarchy ORDER BY id DESC")
#     data = cur.fetchall(); cur.close(); conn.close()
#     return jsonify(data)

# @app.route('/add_merchant', methods=['POST'])
# def add_merchant():
#     data = request.json
#     conn = get_db_connection(); cur = conn.cursor()
#     cur.execute("INSERT INTO merchant_hierarchy (name, region) VALUES (%s, %s)", (data['name'], data['region']))
#     conn.commit(); cur.close(); conn.close()
#     return jsonify({"status": "success"}), 201

# @app.route('/get_merchant_details/<int:group_id>', methods=['GET'])
# def get_details(group_id):
#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     if group_id == 0:
#         cur.execute("SELECT * FROM merchants ORDER BY id DESC")
#     else:
#         cur.execute("SELECT * FROM merchants WHERE group_id = %s ORDER BY id DESC", (group_id,))
#     data = cur.fetchall()
#     cur.close(); conn.close()
#     return jsonify(data)

# @app.route('/add_merchant_detail', methods=['POST'])
# def add_detail():
#     data = request.json
#     conn = get_db_connection(); cur = conn.cursor()
#     cur.execute("INSERT INTO merchants (group_id, name, region, email) VALUES (%s, %s, %s, %s)",
#                 (data['group_id'], data['name'], data['region'], data['email']))
#     conn.commit(); cur.close(); conn.close()
#     return jsonify({"status": "success"}), 201

# @app.route('/get_seasons')
# def get_seasons():
#     conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT * FROM seasons ORDER BY id DESC")
#     data = cur.fetchall(); cur.close(); conn.close()
#     return jsonify(data)

# @app.route('/add_season', methods=['POST'])
# def add_season():
#     data = request.json
#     conn = get_db_connection(); cur = conn.cursor()
#     cur.execute("INSERT INTO seasons (season_name, description) VALUES (%s, %s)",
#                 (data['name'], data['description']))
#     conn.commit(); cur.close(); conn.close()
#     return jsonify({"status": "success"})

# @app.route('/update_season/<int:id>', methods=['PUT'])
# def update_season(id):
#     data = request.json
#     try:
#         conn = get_db_connection(); cur = conn.cursor()
#         cur.execute("UPDATE seasons SET season_name=%s, description=%s WHERE id=%s", 
#                     (data['name'], data['description'], id))
#         conn.commit(); cur.close(); conn.close()
#         return jsonify({"status": "success"}), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route('/place_order', methods=['POST'])
# def place_order():
#     data = request.json
#     username = session.get('user', 'MOHIT')
#     conn = get_db_connection(); cur = conn.cursor()
#     try:
#         cur.execute("UPDATE products SET stock = stock - %s WHERE name = %s AND stock >= %s", 
#                     (data['qty'], data['name'], data['qty']))
#         if cur.rowcount == 0: return jsonify({"status": "error", "message": "Out of stock"}), 400
        
#         cur.execute("""INSERT INTO orders (product_name, quantity, status, order_date, user_id)
#                        VALUES (%s, %s, 'Pending', CURRENT_TIMESTAMP, (SELECT id FROM users WHERE username = %s LIMIT 1))""",
#                     (data['name'], data['qty'], username))
#         conn.commit()
#         return jsonify({"status": "success"})
#     except Exception as e:
#         conn.rollback(); return jsonify({"status": "error", "message": str(e)}), 500
#     finally: cur.close(); conn.close()

# @app.route('/get_orders')
# def get_orders():
#     conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("""SELECT o.id, u.username, o.product_name as product, o.quantity as qty, o.status, o.order_date as date 
#                    FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.order_date DESC""")
#     rows = cur.fetchall(); cur.close(); conn.close()
#     return jsonify(rows)

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from functools import wraps
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/fix_db')
def fix_db():
    conn = get_db_connection(); cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS image TEXT;")
        cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS rating INTEGER DEFAULT 5;")
        
        cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_amount DECIMAL(10,2);")
        cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id INTEGER;")
        cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'Completed';")
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS "Cart" (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER,
                price DECIMAL(10,2)
            );
        """)
        conn.commit()
        return "Database synchronized successfully!"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        cur.close(); conn.close()

@app.route('/')
def dashboard_page():
    return render_template('m.html', user=session.get('user', 'Guest'))

@app.route('/product')
@login_required
def show_products():
    return render_template('Product.html')

@app.route('/cart')
@login_required
def cart_page():
    return render_template('cart.html')

@app.route('/inventory')
@login_required
def inventory_page():
    return render_template('inventory.html')

@app.route('/orders')
@login_required
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
    """Pulls menu names and routes exactly matching your SQL image."""
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT name, route FROM menu ORDER BY id ASC")
    menu_items = cur.fetchall(); cur.close(); conn.close()
    return jsonify(menu_items)

@app.route('/get_products')
def get_products():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM products ORDER BY id DESC")
    products = cur.fetchall(); cur.close(); conn.close()
    return jsonify(products)

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    try:
        name = request.form.get('name'); price = request.form.get('price')
        stock = request.form.get('stock'); category = request.form.get('category')
        file = request.files.get('image_file')
        filename = secure_filename(file.filename) if file and file.filename != '' else 'default.jpg'
        if file and file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO products (name, price, stock, category, image) VALUES (%s, %s, %s, %s, %s)",
                    (name, price, stock, category, filename))
        conn.commit(); cur.close(); conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.get_json()
    items = data.get('items')     
    cust = data.get('customer')   
    user_id = session.get('user_id')
    
    if not items:
        return jsonify({"message": "Cart is empty"}), 400

    total = sum(item['price'] * item['quantity'] for item in items)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # 1. Insert the main order
        cur.execute("""
            INSERT INTO orders (user_id, customer_name, phone_number, address, payment, total_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (user_id, cust['name'], cust['phone'], cust['address'], cust['payment_method'], total, 'paid'))
        
        order_id = cur.fetchone()[0]
        
        # 2. Loop through all items (indented inside try)
        for item in items:
            cur.execute("""
                INSERT INTO Cart_info (order_id, product_name, price_purchase, quantity)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['name'], item['price'], item['quantity']))

        # 3. COMMIT and RETURN must be OUTSIDE the for-loop 
        # but INSIDE the try block.
        conn.commit()
        return jsonify({"message": "Order placed successfully", "order_id": order_id}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Database Error: {e}")
        return jsonify({"message": "Database error", "details": str(e)}), 500
    
@app.route('/get_merchants')
def get_merchants():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM merchant_hierarchy ORDER BY id DESC")
    data = cur.fetchall(); cur.close(); conn.close()
    return jsonify(data)

@app.route('/get_merchant_details/<int:gid>')
def get_details(gid):
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM merchants ORDER BY id DESC" if gid == 0 else "SELECT * FROM merchants WHERE group_id = %s"
    cur.execute(query, (gid,) if gid != 0 else None)
    data = cur.fetchall(); cur.close(); conn.close()
    return jsonify(data)

@app.route('/get_seasons')
def get_seasons():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM seasons ORDER BY id DESC")
    data = cur.fetchall(); cur.close(); conn.close()
    return jsonify(data)

# --- ADD DATA ROUTES ---
@app.route('/add_merchant', methods=['POST'])
def add_merchant():
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO merchant_hierarchy (name, region) VALUES (%s, %s)", (data['name'], data['region']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"})

@app.route('/add_merchant_detail', methods=['POST'])
def add_detail():
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO merchants (group_id, name, region, email) VALUES (%s, %s, %s, %s)",
                (data['group_id'], data['name'], data['region'], data['email']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"})

@app.route('/add_season', methods=['POST'])
def add_season():
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO seasons (season_name, description) VALUES (%s, %s)", (data['name'], data['description']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"})

@app.route('/get_orders')
@login_required
def get_orders():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = """
    SELECT 
        o.id, 
        o.customer_name, 
        o.status, 
        o.address,
        o.total_amount, 
        TO_CHAR(o.order_date, 'YYYY-MM-DD HH24:MI:SS') as date 
    FROM orders o 
    WHERE o.customer_name IS NOT NULL
    ORDER BY o.id DESC
"""
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Could not fetch orders"}), 500
    
    finally:
        if conn:
            conn.close()
if __name__ == '__main__':
    app.run(debug=True)
    
 