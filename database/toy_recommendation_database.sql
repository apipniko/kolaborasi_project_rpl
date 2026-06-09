CREATE DATABASE IF NOT EXISTS toy_recommendation_db;
USE toy_recommendation_db;

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(20),
    rating FLOAT,
    interaction_count INT
);
CREATE TABLE category (
    category_id INT PRIMARY KEY,
    category VARCHAR(100)
);
CREATE TABLE sub_category (
    sub_category_id INT PRIMARY KEY,
    category_id INT,
    sub_category VARCHAR(100),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
CREATE TABLE product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    brand VARCHAR(100),
    price DECIMAL(10,2),
    sub_category_id INT,
    image_filename VARCHAR(255),
    FOREIGN KEY (sub_category_id) REFERENCES sub_category(sub_category_id)
);
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    order_status VARCHAR(50),
    order_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TABLE order_items (
    order_item_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    item_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
