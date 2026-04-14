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
import psycopg2.extras

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "r_global_key"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    """Syncs database tables and initializes the Master menu."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);")
        cur.execute("CREATE TABLE IF NOT EXISTS menu (id SERIAL PRIMARY KEY, name TEXT NOT NULL, route TEXT NOT NULL);")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS merchant_hierarchy (
            id SERIAL PRIMARY KEY, name TEXT NOT NULL, region TEXT);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS merchants (
            id SERIAL PRIMARY KEY, 
            group_id INTEGER REFERENCES merchant_hierarchy(id) ON DELETE CASCADE,
            name TEXT, region TEXT, email TEXT);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS design_sampling (
            id SERIAL PRIMARY KEY, 
            req_id TEXT, 
            buyer_group TEXT, 
            buyer_detail TEXT, 
            sample_type TEXT, 
            fabric TEXT, 
            deadline DATE, 
            remarks TEXT, 
            status TEXT DEFAULT 'Tracking',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS sampling_items (
            id SERIAL PRIMARY KEY, 
            sampling_parent_id INTEGER REFERENCES design_sampling(id) ON DELETE CASCADE,
            size TEXT, 
            quantity INTEGER DEFAULT 0, 
            color TEXT, 
            width TEXT);""")

        # 5. Production & Orders
        cur.execute("""CREATE TABLE IF NOT EXISTS cutting (
            id SERIAL PRIMARY KEY, sampling_id INTEGER REFERENCES design_sampling(id),
            layer_count INTEGER, assigned_by TEXT, assigned_to TEXT, status TEXT, start_date TIMESTAMP);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY, name TEXT, price DECIMAL(10,2), 
            stock INTEGER DEFAULT 0, category TEXT, image TEXT);""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY, user_id INTEGER, customer_name TEXT, 
            phone_number TEXT, address TEXT, payment TEXT, 
            total_amount DECIMAL(10,2), status TEXT DEFAULT 'Paid',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS "Cart" (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER,
                price DECIMAL(10,2)
            );
        """)
        
        cur.execute("INSERT INTO users (username, password) VALUES ('admin', '1234') ON CONFLICT DO NOTHING;")
        cur.execute("SELECT COUNT(*) FROM menu")
        if cur.fetchone()[0] == 0:
            cur.execute("""INSERT INTO menu (name, route) VALUES 
                ('Dashboard', '/'), ('Design', '/design'), ('Product', '/product'), 
                ('Inventory', '/inventory'), ('Orders', '/orders')""")
        
        conn.commit()
        return "All tables (including Groups and Details) verified!"
    except Exception as e:
        conn.rollback()
        return f"Database Error: {str(e)}"
    finally:
        cur.close(); conn.close()
      

@app.route('/')
def dashboard_page():
    return render_template('m.html', user=session.get('user', 'Guest'))

@app.route('/design')
@login_required
def design_page():
    return render_template('design.html', user=session.get('user', 'User'))

@app.route('/product')
@login_required
def show_products():
    return render_template('Product.html')

@app.route('/inventory')
@login_required
def inventory_page():
    return render_template('inventory.html')

@app.route('/get_merchants', methods=['GET'])
def get_merchants():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM merchant_hierarchy ORDER BY id DESC")
    data = cur.fetchall(); cur.close(); conn.close()
    return jsonify(data)

@app.route('/add_merchant', methods=['POST'])
def add_merchant():
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO merchant_hierarchy (name, region) VALUES (%s, %s)", (data['name'], data['region']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/get_merchant_details/<int:group_id>', methods=['GET'])
def get_details(group_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if group_id == 0:
        cur.execute("SELECT * FROM merchants ORDER BY id DESC")
    else:
        cur.execute("SELECT * FROM merchants WHERE group_id = %s ORDER BY id DESC", (group_id,))
    data = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(data)

@app.route('/add_merchant_detail', methods=['POST'])
def add_detail():
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO merchants (group_id, name, region, email) VALUES (%s, %s, %s, %s)",
                (data['group_id'], data['name'], data['region'], data['email']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/get_seasons')
def get_seasons():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM seasons ORDER BY id DESC")
    data = cur.fetchall(); cur.close(); conn.close()
    return jsonify(data)

@app.route('/add_season', methods=['POST'])
def add_season():
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO seasons (season_name, description) VALUES (%s, %s)",
                (data['name'], data['description']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"})

@app.route('/update_season/<int:id>', methods=['PUT'])
def update_season(id):
    data = request.json
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("UPDATE seasons SET season_name=%s, description=%s WHERE id=%s", 
                    (data['name'], data['description'], id))
        conn.commit(); cur.close(); conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/orders')
@login_required
def order_page():
    return render_template('order.html')

@app.route('/cart')
@login_required
def cart_page():
    return render_template('cart.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT id, username FROM users WHERE username = %s AND password = %s",
                    (data['username'], data['password']))
        user = cur.fetchone(); cur.close(); conn.close()
        if user:
            session['user'] = user[1]
            session['user_id'] = user[0]
            return jsonify({"status": "success", "redirect": "/"})
        return jsonify({"status": "error", "message": "Invalid Credentials"}), 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/get_menu')
def get_menu():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT name, route FROM menu ORDER BY id ASC")
    menu_items = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(menu_items)

@app.route('/get_design_data/design_sampling')
def get_design_sampling_data():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute("""
        SELECT ds.*, 
        COALESCE(json_agg(si.*) FILTER (WHERE si.id IS NOT NULL), '[]') as items
        FROM design_sampling ds
        LEFT JOIN sampling_items si ON ds.id = si.sampling_parent_id
        GROUP BY ds.id
        ORDER BY ds.id DESC
    """)
    
    data = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(data)

@app.route('/get_design_data/<view>')
def get_design_data(view):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        h.id, 
                        h.req_id, 
                        h.buyer_group, 
                        h.buyer_detail, -- Make sure this is selected
                        h.sample_type, 
                        h.fabric, 
                        TO_CHAR(h.deadline, 'YYYY-MM-DD') as deadline, 
                        h.status, 
                        h.remarks,
                        i.size, i.quantity, i.color, i.width
                    FROM design_sampling h
                    LEFT JOIN sampling_items i ON h.id = i.sampling_parent_id
                    ORDER BY h.id DESC
                """)
                return jsonify(cur.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_design_entry', methods=['POST'])
def add_design_entry():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Insert main record
        cur.execute("""INSERT INTO design_sampling 
            (req_id, buyer_group, buyer_detail, sample_type, fabric, deadline, remarks, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (data['req_id'], data['buyer_group'], data['buyer_detail'], 
             data['sample_type'], data['fabric'], data['deadline'] or None, 
             data['remarks'], data.get('status', 'Tracking')))
        
        parent_id = cur.fetchone()[0]

        # Insert items
        if 'items' in data:
            for item in data['items']:
                cur.execute("""INSERT INTO sampling_items (sampling_parent_id, color, quantity, size)
                            VALUES (%s, %s, %s, %s)""",
                            (parent_id, item['color'], item['quantity'], item['size']))
        
        conn.commit()
        return jsonify({"status": "success", "id": parent_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cur.close(); conn.close()

@app.route('/update_design_entry/<int:id>', methods=['PUT'])
def update_design_entry(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 1. Handle Status Update (The "Move to Cutting" or "Finish" action)
        if 'status' in data and len(data) == 1:
            # FIX: Changed 'db_id' to 'id' to match the route parameter
            cur.execute("UPDATE design_sampling SET status = %s WHERE id = %s", 
                        (data.get('status'), id))
        
        # 2. Handle Full Edit (The "Pencil Icon" update)
        else:
            cur.execute("""UPDATE design_sampling SET 
                buyer_group=%s, buyer_detail=%s, sample_type=%s, fabric=%s, 
                deadline=%s, remarks=%s WHERE id=%s""",
                (data['buyer_group'], data['buyer_detail'], data['sample_type'], 
                 data['fabric'], data['deadline'] or None, data['remarks'], id))
            
            # Refresh items for this specific unique ID
            cur.execute("DELETE FROM sampling_items WHERE sampling_parent_id = %s", (id,))
            if 'items' in data:
                for item in data['items']:
                    cur.execute("""INSERT INTO sampling_items (sampling_parent_id, color, quantity, size)
                                VALUES (%s, %s, %s, %s)""",
                                (id, item['color'], item['quantity'], item['size']))
        
        conn.commit()
        return jsonify({"status": "success"})
    
    except Exception as e:
        conn.rollback()
        print(f"Database Error: {e}") 
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cur.close()
        conn.close()
    
@app.route('/move_to_cutting/<int:id>', methods=['POST'])
@login_required
def move_to_cutting(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE design_sampling SET status = 'Cutting' WHERE id = %s", (id,))
                conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_cutting', methods=['POST'])
@login_required
def add_cutting():
    data = request.json
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO cutting (sampling_id, layer_count, assigned_by, assigned_to, status, start_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    data.get('sampling_id'),
                    data.get('layer_count'),
                    data.get('assigned_by'),
                    data.get('assigned_to'),
                    data.get('status'),
                    data.get('start_date') if data.get('start_date') else None
                ))
                conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/remove_constraint')
def remove_constraint():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE design_sampling DROP CONSTRAINT IF EXISTS design_sampling_req_id_key;")
        conn.commit()
        return "Constraint removed! You can now use duplicate IDs."
    except Exception as e:
        return str(e)
    finally:
        cur.close(); conn.close()

@app.route('/forward_design_entry/<int:id>', methods=['POST'])
@login_required
def forward_design_entry(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE design_sampling SET status = 'Received' WHERE id = %s", (id,))
                conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/update_design_entry/<int:id>', methods=['PUT'])
# @login_required
# def update_design_entry(id):
#     data = request.json
#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as cur:
#                 query = """
#                     UPDATE design_sampling 
#                     SET buyer=%s, detail=%s, fabric=%s, type=%s, deadline=%s, name=%s
#                     WHERE id=%s
#                 """
#                 cur.execute(query, (
#                     data.get('buyer'), data.get('detail'), data.get('fabric'),
#                     data.get('sample_type'), data.get('deadline'), data.get('req_id'), id
#                 ))
#                 conn.commit()
#                 return jsonify({"status": "success"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
@app.route('/get_cutting_history')
@login_required
def get_cutting_history():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT c.*, d.name as sample_name 
            FROM cutting c
            JOIN design_sampling d ON c.sampling_id = d.id
            ORDER BY c.id DESC
        """)
        data = cur.fetchall()
        cur.close(); conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify([])
    
@app.route('/complete_cutting/<int:id>', methods=['POST'])
@login_required
def complete_cutting(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE cutting SET status = 'Completed' WHERE id = %s", (id,))
                conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 500
    
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
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category = request.form.get('category')
        file = request.files.get('image_file')
        filename = secure_filename(file.filename) if file else 'default.jpg'
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO products (name, price, stock, category, image) VALUES (%s, %s, %s, %s, %s)",
                    (name, price, stock, category, filename))
        conn.commit(); cur.close(); conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update_stock', methods=['POST'])
@login_required
def update_stock():
    data = request.json
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("UPDATE products SET stock = %s WHERE id = %s", (data['stock'], data['id']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"status": "success"})

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.get_json()
    items = data.get('items'); cust = data.get('customer')
    user_id = session.get('user_id')
    if not items: return jsonify({"message": "Cart empty"}), 400

    conn = get_db_connection(); cur = conn.cursor()
    try:
        total = sum(float(item['price']) * int(item['quantity']) for item in items)
        cur.execute("""INSERT INTO orders (user_id, customer_name, phone_number, address, payment, total_amount)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""", 
                    (user_id, cust['name'], cust['phone'], cust['address'], cust['payment_method'], total))
        order_id = cur.fetchone()[0]

        for item in items:
            cur.execute("""INSERT INTO "Cart_info" (order_id, product_name, price_purchase, quantity)
                           VALUES (%s, %s, %s, %s)""", (order_id, item['name'], item['price'], item['quantity']))
            cur.execute("UPDATE products SET stock = stock - %s WHERE name = %s", (item['quantity'], item['name']))

        conn.commit()
        return jsonify({"message": "Order success", "order_id": order_id}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Error", "details": str(e)}), 500
    finally:
        cur.close(); conn.close()

@app.route('/get_orders')
@login_required
def get_orders():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, customer_name, status, Address, total_amount, TO_CHAR(order_date, 'YYYY-MM-DD HH24:MI') as date FROM orders ORDER BY id DESC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
    
    

