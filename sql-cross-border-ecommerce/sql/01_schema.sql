-- ============================================================
-- 跨境电商独立站数据库设计
-- 品牌：DTC 美妆品牌出海（北美 + 东南亚市场）
-- ============================================================

-- 用户表
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    country VARCHAR(50),           -- 国家：US, CA, ID, TH, MY...
    region VARCHAR(20),            -- 市场：North America, Southeast Asia
    language VARCHAR(20) DEFAULT 'en',
    registration_date DATE,
    channel_source VARCHAR(50),    -- 注册来源：Organic, Social Media, KOL, Paid Ads
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 商品表
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200),
    category VARCHAR(50),          -- Lipstick, Skincare, Foundation...
    sub_category VARCHAR(50),
    unit_price DECIMAL(10, 2),     -- 售价 USD
    cost_price DECIMAL(10, 2),     -- 成本 USD
    weight_grams INT,
    is_halal_certified BOOLEAN DEFAULT FALSE,  -- 清真认证（东南亚市场必需）
    launch_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单主表
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    order_status VARCHAR(20) DEFAULT 'pending',  -- pending, shipped, delivered, cancelled, returned
    total_amount DECIMAL(10, 2),
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    shipping_country VARCHAR(50),
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    currency VARCHAR(10) DEFAULT 'USD',
    payment_method VARCHAR(30),
    campaign_id INT,               -- 关联营销活动
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 订单明细表
CREATE TABLE order_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10, 2),     -- 下单时单价
    total_price DECIMAL(10, 2),    -- quantity * unit_price
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 库存表
CREATE TABLE inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    warehouse_location VARCHAR(50), -- LA, NY, Singapore, Jakarta...
    quantity INT DEFAULT 0,
    safety_stock INT DEFAULT 10,
    last_restock_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 营销活动表
CREATE TABLE marketing_campaigns (
    campaign_id INT PRIMARY KEY AUTO_INCREMENT,
    campaign_name VARCHAR(200),
    campaign_type VARCHAR(50),     -- EDM, KOL, Social Media, Paid Ads, Seasonal
    channel VARCHAR(50),
    target_region VARCHAR(20),     -- North America, Southeast Asia, All
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10, 2),
    actual_spend DECIMAL(10, 2),
    revenue_generated DECIMAL(10, 2),
    new_customers_acquired INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引优化
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_country ON orders(shipping_country);
CREATE INDEX idx_customers_region ON customers(region);
CREATE INDEX idx_customers_country ON customers(country);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_campaigns_region ON marketing_campaigns(target_region);
