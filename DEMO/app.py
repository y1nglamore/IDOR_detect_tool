import sqlite3
from flask import *
import os 
from functools import wraps
import time

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DATABASE'] = 'shop.db'
app.config['SECRET_KEY'] = 'cd0ed627-6057-dce6-cd73-79860777655e'

# 初始化数据库
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('shop.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# 获取数据库连接
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

# 登录拦截装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'message': '请先登录', 'timestamp': time.time() * 10000, 'code': 401, 'status': 'error'})
        return f(*args, **kwargs)
    return decorated_function

# 关闭数据库连接
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def f_login():
    if 'username' in session:
        return f"<script>alert('欢迎回来，{session['username']}');location.href='/dashboard';</script>"
    else:
        return render_template('login.html')
    
@app.route('/register')
def f_register():
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def f_dashboard():
    return render_template('dashboard.html')

@app.route('/orders')
@login_required
def f_orders():
    return render_template('orders.html')

@app.route('/coupons')
@login_required
def f_coupons():
    return render_template('coupons.html')

@app.route('/logout')
@login_required
def f_logout():
    session.pop('username', None)
    return redirect(url_for('f_login'))

@app.route('/checkout')
@login_required
def f_checkout():
    return render_template('checkout.html')

# 注册路由
@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

    db = sqlite3.connect(app.config['DATABASE'])
    # 判断用户名是否已存在
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
    if user := cursor.fetchone():
        return jsonify({'message': '用户名已存在', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

    try:
        cursor = db.cursor()
        cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        # 为该用户生成3个优惠券
        userid = cursor.lastrowid
        for _ in range(3):
            cursor.execute('INSERT INTO coupon (user_id, code, amount, reusable) VALUES (?, ?, ?, ?)', (userid, os.urandom(16).hex(), 20.00, 1))
        db.commit()

        user_id = cursor.lastrowid
        return jsonify({'message': '注册成功', 'user_id': user_id, 'timestamp': time.time() * 10000, 'code': 200, 'status': 'success'})
    except:
        db.rollback()
        return jsonify({'message': '注册失败', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

# 登录路由
@app.route('/api/login', methods=['POST'])
def login():  # sourcery skip: use-named-expression

    if 'username' in session:
        return jsonify({'message': '您已是登录状态，如需重新登陆请先退出原账号', 'timestamp': time.time() * 10000, 'code': 200, 'status': 'success'})

    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        session['username'] = username  
        return jsonify({'message': '登录成功', 'timestamp': time.time() * 10000, 'code': 200, 'status': 'success'})
    else:
        return jsonify({'message': '用户名或密码不正确', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})


# 列出所有商品路由
@app.route('/api/shop/product/list', methods=['GET'])
@login_required
def list_products():
    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute('SELECT id, name, price FROM product')
    products = [{'id': row[0], 'name': row[1], 'price': row[2]} for row in cursor.fetchall()]
    db.close()
    return jsonify(products)

# 查看商品详情路由
@app.route('/api/shop/product/detail', methods=['GET'])
@login_required
def product_detail():
    product_id = request.args.get('product_id')

    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()

    # 查询商品信息
    cursor.execute('SELECT id, name, price FROM product WHERE id = ?', (product_id,))
    if product := cursor.fetchone():
        product_detail = {
            'id': product[0],
            'name': product[1],
            'price': product[2]
        }
        db.close()
        return jsonify(product_detail)
    else:
        db.close()
        return jsonify({'message': '商品不存在', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

# 购买商品路由 漏洞：越权使用全网任意用户的优惠券 -> 0元购
@app.route('/api/shop/product/buy', methods=['POST'])
@login_required
def buy_product():
    product_id = request.json.get('product_id')
    coupon_code = request.json.get('coupon_code')

    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()

    # 判断优惠券是否存在
    if coupon_code:
        cursor.execute('SELECT * FROM coupon WHERE code = ?', (coupon_code,))
        if not cursor.fetchone():
            return jsonify({'message': f'优惠券{coupon_code}不存在', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

    # 获取商品价格
    cursor.execute('SELECT price FROM product WHERE id = ?', (product_id,))
    product_price = cursor.fetchone()[0]

    # 获取用户余额
    user_balance = 0.00
    username = session.get('username')
    cursor.execute('SELECT balance FROM user WHERE username = ?', (username,))
    if result := cursor.fetchone():
        user_balance = result[0]
        

    # 获取优惠券额度
    coupon_amount = 0.00
    if coupon_code:
        cursor.execute('SELECT amount FROM coupon WHERE code = ?', (coupon_code,))
        coupon_amount = cursor.fetchone()[0]

    # 判断余额是否足够
    total_amount = product_price - coupon_amount
    if total_amount <= 0:
        total_amount = 0.00

    if user_balance >= total_amount:
        # 减少余额
        user_balance -= total_amount

        # 更新用户余额
        cursor.execute('UPDATE user SET balance = ? WHERE username = ?', (user_balance, username))

        # 生成订单
        user_id = cursor.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone()[0]
        cursor.execute('INSERT INTO `order` (user_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                       (user_id, product_id, 1, total_amount))  
        db.commit()
        db.close()
        if coupon_code:
            return jsonify({'message': f'successfully to buy with coupon [{coupon_code}]  ', 'order_id': cursor.lastrowid, 'timestamp': time.time() * 10000, 'code': 200, 'status': 'success'})
        else:
            return jsonify({'message': '购买成功', 'order_id': cursor.lastrowid, 'timestamp': time.time() * 10000, 'code': 200, 'status': 'success'})
    else:
        db.close()
        return jsonify({'message': '余额不足', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

# 列出优惠券路由
@app.route('/api/shop/coupon/list', methods=['GET'])
@login_required
def list_coupons():
    username = session['username']
    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute('SELECT id, code, amount, reusable FROM coupon WHERE user_id = (SELECT id FROM user WHERE username = ?)', (username,))
    coupons = [{'id': row[0], 'code': row[1], 'amount': row[2], 'reusable': bool(row[3])} for row in cursor.fetchall()]
    db.close()
    print(coupons)
    return jsonify(coupons)

# 列出订单路由
@app.route('/api/shop/order/list', methods=['GET'])
@login_required
def list_orders():
    username = session['username']
    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute('SELECT id, user_id, product_id, quantity, price FROM `order` WHERE user_id = (SELECT id FROM user WHERE username = ?)', (username,))
    orders = [{'id': row[0], 'user_id': row[1], 'product_id': row[2], 'quantity': row[3], 'price': row[4]} for row in cursor.fetchall()]
    db.close()
    return jsonify(orders)

# 查看订单详情路由 漏洞：越权查看任意订单
@app.route('/api/shop/order/detail', methods=['GET'])
@login_required
def order_detail():
    order_id = request.args.get('order_id')

    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()

    # 查询订单信息
    cursor.execute('SELECT id, user_id, product_id, quantity, price FROM `order` WHERE id = ?', (order_id,))
    order = cursor.fetchone()

    if order:
        order_detail = {
            'id': order[0],
            'user_id': order[1],
            'product_id': order[2],
            'quantity': order[3],
            'price': order[4]
        }
        db.close()
        return jsonify({'message': 'get order detail information successfully', 'data': order_detail, 'timestamp': time.time() * 10000, 'code': 200, 'status': 'success'})
    else:
        db.close()
        return jsonify({'message': '订单不存在', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})


# 删除订单路由
@app.route('/api/shop/order/delete', methods=['POST'])
@login_required
def delete_order():
    order_id = request.json.get('order_id')
    username = session['username']

    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()

    # 检查订单是否存在并属于当前用户
    cursor.execute('SELECT user_id FROM `order` WHERE id = ?', (order_id,))
    result = cursor.fetchone()
    if not result:
        db.close()
        return jsonify({'message': '订单不存在或无权限删除该订单', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})
    user_id = result[0]
    current_user_id = cursor.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone()[0]
    if user_id != current_user_id:
        db.close()
        return jsonify({'message': '订单不存在或无权限删除该订单', 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

    # 执行删除操作
    cursor.execute('DELETE FROM `order` WHERE id = ?', (order_id,))
    db.commit()
    db.close()
    return jsonify({'message': '订单删除成功', 'timestamp': time.time() * 10000, 'code': 200, 'status': 'success'})

# 获取余额路由
@app.route('/api/user/balance', methods=['GET'])
@login_required
def get_balance():
    username = session['username']

    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()

    # 查询用户余额
    cursor.execute('SELECT balance FROM user WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        balance = result[0]
        db.close()
        return jsonify({'balance': balance})
    else:
        db.close()
        return jsonify({'message': '获取用户余额失败', 'balance': 0.00, 'timestamp': time.time() * 10000, 'code': 500, 'status': 'error'})

if __name__ == '__main__':
    app.run(port=5888)
