-- 用户表
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 用户id（自增）
    username TEXT NOT NULL, -- 用户名
    password TEXT NOT NULL -- 密码
);

ALTER TABLE user ADD COLUMN balance FLOAT DEFAULT 30.00;

-- 订单表
CREATE TABLE `order` (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 订单ID（自增）
    user_id INTEGER, -- 用户ID
    product_id INTEGER, -- 商品ID
    quantity INTEGER, -- 数量
    price FLOAT, -- 价格
    FOREIGN KEY (user_id) REFERENCES user(id), -- 外键关联到user表的id字段
    FOREIGN KEY (product_id) REFERENCES product(id) -- 外键关联到product表的id字段
);

-- 优惠券表
CREATE TABLE coupon (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 优惠券ID（自增）
    user_id INTEGER, -- 用户ID
    code TEXT, -- 优惠券代码
    amount FLOAT, -- 金额
    reusable INTEGER, -- 是否可重复使用
    FOREIGN KEY (user_id) REFERENCES user(id) -- 外键关联到user表的id字段
);

-- 商品表
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 商品ID（自增）
    name TEXT, -- 商品名称
    price FLOAT -- 价格
);



INSERT INTO user (id, username, password) VALUES (1, 'admin', 'admin@123');

INSERT INTO product (name, price) VALUES ('Shoe', 24.99);
INSERT INTO product (name, price) VALUES ('T-shirt', 19.99);
INSERT INTO product (name, price) VALUES ('Jeans', 37.50);
INSERT INTO product (name, price) VALUES ('Hat', 8.75);
INSERT INTO product (name, price) VALUES ('Socks', 42.25);

INSERT INTO coupon (user_id, code, amount, reusable, user_id) VALUES (1, 'ADMIN50OFF', 50, 1, 1);