-- ============================================================
-- 示例数据：跨境电商独立站
-- 约 100 用户、200 订单、20 商品、4 营销活动
-- ============================================================

-- 用户数据（30条代表性数据）
INSERT INTO customers (customer_id, name, email, country, region, registration_date, channel_source) VALUES
(1, 'Emily Chen', 'emily.c@email.com', 'US', 'North America', '2024-01-15', 'Organic'),
(2, 'Sarah Johnson', 'sarah.j@email.com', 'US', 'North America', '2024-02-20', 'Social Media'),
(3, 'Jessica Williams', 'jessica.w@email.com', 'US', 'North America', '2024-03-10', 'KOL'),
(4, 'Amanda Brown', 'amanda.b@email.com', 'US', 'North America', '2024-01-05', 'Paid Ads'),
(5, 'Michelle Davis', 'michelle.d@email.com', 'CA', 'North America', '2024-02-14', 'Organic'),
(6, 'Lisa Wilson', 'lisa.w@email.com', 'CA', 'North America', '2024-03-01', 'Social Media'),
(7, 'Jennifer Taylor', 'jennifer.t@email.com', 'US', 'North America', '2024-04-05', 'EDM'),
(8, 'Nicole Anderson', 'nicole.a@email.com', 'US', 'North America', '2024-01-20', 'KOL'),
(9, 'Rachel Martinez', 'rachel.m@email.com', 'US', 'North America', '2024-02-28', 'Organic'),
(10, 'Stephanie Thomas', 'stephanie.t@email.com', 'CA', 'North America', '2024-03-15', 'Social Media'),
(11, 'Siti Nurhaliza', 'siti.n@email.com', 'ID', 'Southeast Asia', '2024-01-10', 'TikTok'),
(12, 'Dewi Lestari', 'dewi.l@email.com', 'ID', 'Southeast Asia', '2024-02-05', 'Shopee'),
(13, 'Putri Ayu', 'putri.a@email.com', 'ID', 'Southeast Asia', '2024-03-20', 'KOL'),
(14, 'Nurul Hidayah', 'nurul.h@email.com', 'MY', 'Southeast Asia', '2024-01-25', 'TikTok'),
(15, 'Aisha Tan', 'aisha.t@email.com', 'MY', 'Southeast Asia', '2024-02-10', 'Organic'),
(16, 'Ratna Dewi', 'ratna.d@email.com', 'ID', 'Southeast Asia', '2024-04-01', 'Social Media'),
(17, 'Mawar Indah', 'mawar.i@email.com', 'ID', 'Southeast Asia', '2024-03-05', 'TikTok'),
(18, 'Linh Nguyen', 'linh.n@email.com', 'TH', 'Southeast Asia', '2024-01-30', 'Shopee'),
(19, 'Mai Pham', 'mai.p@email.com', 'TH', 'Southeast Asia', '2024-02-15', 'KOL'),
(20, 'Somsak Chai', 'somsak.c@email.com', 'TH', 'Southeast Asia', '2024-03-25', 'TikTok'),
(21, 'Ashley Kim', 'ashley.k@email.com', 'US', 'North America', '2024-05-01', 'Organic'),
(22, 'Brittany Lee', 'brittany.l@email.com', 'US', 'North America', '2024-05-10', 'Paid Ads'),
(23, 'Catherine Park', 'catherine.p@email.com', 'CA', 'North America', '2024-05-15', 'Social Media'),
(24, 'Diana Garcia', 'diana.g@email.com', 'US', 'North America', '2024-06-01', 'EDM'),
(25, 'Erika Lopez', 'erika.l@email.com', 'US', 'North America', '2024-06-10', 'KOL'),
(26, 'Intan Permata', 'intan.p@email.com', 'ID', 'Southeast Asia', '2024-05-05', 'TikTok'),
(27, 'Bunga Citra', 'bunga.c@email.com', 'ID', 'Southeast Asia', '2024-05-20', 'Shopee'),
(28, 'Melati Kusuma', 'melati.k@email.com', 'MY', 'Southeast Asia', '2024-06-01', 'Social Media'),
(29, 'Anggun Sari', 'anggun.s@email.com', 'ID', 'Southeast Asia', '2024-06-15', 'TikTok'),
(30, 'Chaya Wattana', 'chaya.w@email.com', 'TH', 'Southeast Asia', '2024-06-20', 'KOL');

-- 商品数据
INSERT INTO products (product_id, product_name, category, sub_category, unit_price, cost_price, weight_grams, is_halal_certified, launch_date) VALUES
(1, 'Velvet Matte Lipstick - Rose', 'Lipstick', 'Matte', 22.00, 8.00, 35, TRUE, '2024-01-01'),
(2, 'Velvet Matte Lipstick - Coral', 'Lipstick', 'Matte', 22.00, 8.00, 35, TRUE, '2024-01-01'),
(3, 'Velvet Matte Lipstick - Berry', 'Lipstick', 'Matte', 22.00, 8.00, 35, TRUE, '2024-03-01'),
(4, 'Hydra Glow Foundation - Fair', 'Foundation', 'Liquid', 35.00, 12.00, 80, FALSE, '2024-01-01'),
(5, 'Hydra Glow Foundation - Natural', 'Foundation', 'Liquid', 35.00, 12.00, 80, FALSE, '2024-01-01'),
(6, 'Hydra Glow Foundation - Tan', 'Foundation', 'Liquid', 35.00, 12.00, 80, FALSE, '2024-03-01'),
(7, 'Sunset Eyeshadow Palette', 'Eyeshadow', 'Palette', 42.00, 15.00, 200, TRUE, '2024-02-01'),
(8, 'Waterproof Eyeliner - Black', 'Eyeliner', 'Liquid', 18.00, 5.00, 25, TRUE, '2024-01-01'),
(9, 'Waterproof Eyeliner - Brown', 'Eyeliner', 'Liquid', 18.00, 5.00, 25, TRUE, '2024-01-01'),
(10, 'Sun Screen SPF50+', 'Skincare', 'Sunscreen', 28.00, 10.00, 60, TRUE, '2024-01-01'),
(11, 'Brightening Serum', 'Skincare', 'Serum', 45.00, 18.00, 50, TRUE, '2024-02-01'),
(12, 'Whitening Day Cream', 'Skincare', 'Cream', 32.00, 12.00, 80, TRUE, '2024-01-01'),
(13, 'Clean Beauty Cleanser', 'Skincare', 'Cleanser', 25.00, 8.00, 120, FALSE, '2024-03-01'),
(14, 'Lip Gloss - Clear', 'Lipstick', 'Gloss', 15.00, 5.00, 25, TRUE, '2024-04-01'),
(15, 'Mini Lipstick Set (3 pcs)', 'Lipstick', 'Set', 48.00, 18.00, 100, TRUE, '2024-05-01'),
(16, 'Travel Skincare Kit', 'Skincare', 'Set', 55.00, 22.00, 250, TRUE, '2024-05-01'),
(17, 'Blush Duo - Peach & Pink', 'Blush', 'Duo', 28.00, 10.00, 45, TRUE, '2024-04-01'),
(18, 'Mascara - Volume', 'Mascara', 'Volume', 20.00, 6.00, 30, TRUE, '2024-01-01'),
(19, 'Sheet Mask Set (10 pcs)', 'Skincare', 'Mask', 18.00, 6.00, 200, TRUE, '2024-02-01'),
(20, 'Limited Edition Lunar New Year Set', 'Skincare', 'Set', 68.00, 28.00, 350, TRUE, '2024-01-15');

-- 订单数据（选取部分代表性订单）
INSERT INTO orders (order_id, customer_id, order_date, order_status, total_amount, discount_amount, shipping_country, shipping_cost, payment_method, campaign_id) VALUES
-- 北美高频用户 Emily (customer 1)
(1, 1, '2024-01-20', 'delivered', 57.00, 0, 'US', 5.00, 'Credit Card', NULL),
(2, 1, '2024-02-15', 'delivered', 89.00, 10.00, 'US', 0, 'Credit Card', 1),
(3, 1, '2024-03-20', 'delivered', 126.00, 0, 'US', 5.00, 'Credit Card', NULL),
(4, 1, '2024-04-25', 'delivered', 55.00, 0, 'US', 5.00, 'Credit Card', NULL),
(5, 1, '2024-05-30', 'delivered', 48.00, 5.00, 'US', 0, 'PayPal', 3),
(6, 1, '2024-06-28', 'shipped', 103.00, 0, 'US', 0, 'Credit Card', NULL),
-- 东南亚高频用户 Siti (customer 11)
(7, 11, '2024-01-15', 'delivered', 22.00, 0, 'ID', 3.00, 'GoPay', NULL),
(8, 11, '2024-02-10', 'delivered', 54.00, 5.00, 'ID', 0, 'GoPay', 2),
(9, 11, '2024-03-15', 'delivered', 18.00, 0, 'ID', 3.00, 'GoPay', NULL),
(10, 11, '2024-04-20', 'delivered', 35.00, 0, 'ID', 0, 'GoPay', 2),
(11, 11, '2024-05-25', 'delivered', 22.00, 0, 'ID', 0, 'GoPay', 4),
(12, 11, '2024-06-30', 'shipped', 42.00, 0, 'ID', 0, 'GoPay', NULL),
-- 其他用户订单
(13, 2, '2024-03-01', 'delivered', 22.00, 0, 'US', 5.00, 'Credit Card', NULL),
(14, 2, '2024-04-05', 'delivered', 45.00, 5.00, 'US', 0, 'Credit Card', 1),
(15, 3, '2024-03-15', 'delivered', 42.00, 0, 'US', 5.00, 'PayPal', NULL),
(16, 4, '2024-02-01', 'delivered', 70.00, 0, 'US', 0, 'Credit Card', NULL),
(17, 5, '2024-02-20', 'delivered', 35.00, 0, 'CA', 8.00, 'Credit Card', NULL),
(18, 5, '2024-04-10', 'delivered', 28.00, 0, 'CA', 8.00, 'Credit Card', NULL),
(19, 7, '2024-04-10', 'delivered', 55.00, 10.00, 'US', 0, 'PayPal', 1),
(20, 8, '2024-02-15', 'delivered', 42.00, 0, 'US', 5.00, 'Credit Card', NULL),
(21, 9, '2024-03-20', 'delivered', 25.00, 0, 'US', 5.00, 'PayPal', NULL),
(22, 10, '2024-04-01', 'delivered', 18.00, 0, 'CA', 8.00, 'Credit Card', NULL),
(23, 12, '2024-02-10', 'delivered', 22.00, 3.00, 'ID', 0, 'GoPay', 2),
(24, 12, '2024-03-15', 'delivered', 15.00, 0, 'ID', 3.00, 'GoPay', NULL),
(25, 12, '2024-05-10', 'delivered', 32.00, 0, 'ID', 0, 'ShopeePay', 4),
(26, 13, '2024-04-05', 'delivered', 48.00, 5.00, 'ID', 0, 'GoPay', NULL),
(27, 14, '2024-02-15', 'delivered', 28.00, 0, 'MY', 4.00, 'GrabPay', NULL),
(28, 14, '2024-03-20', 'delivered', 45.00, 0, 'MY', 0, 'GrabPay', 2),
(29, 15, '2024-03-01', 'delivered', 18.00, 0, 'MY', 4.00, 'GrabPay', NULL),
(30, 16, '2024-04-10', 'delivered', 20.00, 0, 'ID', 0, 'GoPay', 4),
(31, 17, '2024-03-10', 'delivered', 32.00, 5.00, 'ID', 0, 'GoPay', 2),
(32, 18, '2024-02-20', 'delivered', 22.00, 0, 'TH', 3.00, 'TrueMoney', NULL),
(33, 18, '2024-04-15', 'delivered', 18.00, 0, 'TH', 3.00, 'TrueMoney', NULL),
(34, 19, '2024-03-01', 'delivered', 55.00, 10.00, 'TH', 0, 'TrueMoney', 2),
(35, 20, '2024-04-20', 'delivered', 25.00, 0, 'TH', 3.00, 'TrueMoney', NULL),
(36, 21, '2024-05-15', 'delivered', 42.00, 0, 'US', 5.00, 'Credit Card', 3),
(37, 22, '2024-05-20', 'delivered', 22.00, 0, 'US', 5.00, 'Credit Card', NULL),
(38, 23, '2024-06-01', 'shipped', 35.00, 5.00, 'CA', 0, 'Credit Card', 3),
(39, 24, '2024-06-15', 'shipped', 48.00, 0, 'US', 0, 'PayPal', NULL),
(40, 25, '2024-06-20', 'shipped', 28.00, 0, 'US', 5.00, 'Credit Card', NULL),
(41, 26, '2024-05-10', 'delivered', 18.00, 3.00, 'ID', 0, 'GoPay', 4),
(42, 27, '2024-06-01', 'shipped', 22.00, 0, 'ID', 0, 'ShopeePay', NULL),
(43, 28, '2024-06-10', 'shipped', 45.00, 5.00, 'MY', 0, 'GrabPay', NULL),
(44, 29, '2024-06-25', 'shipped', 15.00, 0, 'ID', 3.00, 'GoPay', NULL),
(45, 30, '2024-06-30', 'pending', 32.00, 0, 'TH', 0, 'TrueMoney', NULL);

-- 订单明细
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 1, 2, 22.00, 44.00), (1, 8, 1, 18.00, 18.00),
(2, 11, 1, 45.00, 45.00), (2, 13, 1, 25.00, 25.00), (2, 14, 1, 15.00, 15.00),
(3, 7, 1, 42.00, 42.00), (3, 4, 1, 35.00, 35.00), (3, 11, 1, 45.00, 45.00),
(4, 16, 1, 55.00, 55.00),
(5, 15, 1, 48.00, 48.00),
(6, 20, 1, 68.00, 68.00), (6, 2, 1, 22.00, 22.00), (6, 8, 1, 18.00, 18.00),
(7, 1, 1, 22.00, 22.00),
(8, 12, 1, 32.00, 32.00), (8, 2, 1, 22.00, 22.00),
(9, 8, 1, 18.00, 18.00),
(10, 4, 1, 35.00, 35.00),
(11, 1, 1, 22.00, 22.00),
(12, 7, 1, 42.00, 42.00),
(13, 2, 1, 22.00, 22.00),
(14, 11, 1, 45.00, 45.00),
(15, 7, 1, 42.00, 42.00),
(16, 16, 1, 55.00, 55.00), (16, 14, 1, 15.00, 15.00),
(17, 4, 1, 35.00, 35.00),
(18, 10, 1, 28.00, 28.00),
(19, 16, 1, 55.00, 55.00),
(20, 7, 1, 42.00, 42.00),
(21, 13, 1, 25.00, 25.00),
(22, 9, 1, 18.00, 18.00),
(23, 1, 1, 22.00, 22.00),
(24, 14, 1, 15.00, 15.00),
(25, 12, 1, 32.00, 32.00),
(26, 15, 1, 48.00, 48.00),
(27, 10, 1, 28.00, 28.00),
(28, 11, 1, 45.00, 45.00),
(29, 19, 1, 18.00, 18.00),
(30, 18, 1, 20.00, 20.00),
(31, 12, 1, 32.00, 32.00),
(32, 2, 1, 22.00, 22.00),
(33, 19, 1, 18.00, 18.00),
(34, 16, 1, 55.00, 55.00),
(35, 13, 1, 25.00, 25.00),
(36, 7, 1, 42.00, 42.00),
(37, 3, 1, 22.00, 22.00),
(38, 4, 1, 35.00, 35.00),
(39, 15, 1, 48.00, 48.00),
(40, 17, 1, 28.00, 28.00),
(41, 19, 1, 18.00, 18.00),
(42, 1, 1, 22.00, 22.00),
(43, 11, 1, 45.00, 45.00),
(44, 14, 1, 15.00, 15.00),
(45, 12, 1, 32.00, 32.00);

-- 库存数据
INSERT INTO inventory (product_id, warehouse_location, quantity, safety_stock, last_restock_date) VALUES
(1, 'LA', 250, 50, '2024-06-15'), (1, 'Singapore', 150, 30, '2024-06-10'),
(2, 'LA', 180, 40, '2024-06-15'), (2, 'Singapore', 200, 40, '2024-06-10'),
(3, 'LA', 120, 30, '2024-06-01'), (3, 'Singapore', 80, 20, '2024-06-01'),
(4, 'LA', 200, 50, '2024-06-15'), (5, 'LA', 150, 40, '2024-06-15'),
(6, 'Singapore', 90, 25, '2024-06-01'),
(7, 'LA', 100, 30, '2024-06-10'), (7, 'Singapore', 60, 20, '2024-06-10'),
(8, 'LA', 300, 60, '2024-06-20'), (8, 'Singapore', 120, 30, '2024-06-15'),
(10, 'LA', 80, 20, '2024-06-01'), (10, 'Singapore', 200, 40, '2024-06-15'),
(11, 'LA', 90, 25, '2024-06-10'), (11, 'Singapore', 40, 15, '2024-06-10'),
(12, 'Singapore', 150, 30, '2024-06-15'),
(15, 'LA', 60, 20, '2024-06-01'),
(16, 'Singapore', 30, 10, '2024-06-15'),
(20, 'LA', 20, 5, '2024-01-20');

-- 营销活动
INSERT INTO marketing_campaigns (campaign_id, campaign_name, campaign_type, channel, target_region, start_date, end_date, budget, actual_spend, revenue_generated, new_customers_acquired) VALUES
(1, 'Valentine''s Day EDM', 'EDM', 'Email', 'North America', '2024-02-01', '2024-02-14', 2000.00, 1850.00, 8500.00, 45),
(2, 'TikTok Ramadan Beauty', 'Social Media', 'TikTok', 'Southeast Asia', '2024-03-01', '2024-04-10', 3000.00, 2800.00, 12000.00, 120),
(3, 'Summer Glow KOL Campaign', 'KOL', 'Instagram', 'North America', '2024-05-15', '2024-06-15', 5000.00, 4600.00, 18500.00, 80),
(4, 'Shopee 6.6 Mega Sale', 'Seasonal', 'Shopee', 'Southeast Asia', '2024-06-01', '2024-06-10', 1500.00, 1400.00, 6500.00, 95);

-- 更新订单与营销活动的关联
UPDATE orders SET campaign_id = 1 WHERE order_id IN (2, 14, 19);
UPDATE orders SET campaign_id = 2 WHERE order_id IN (8, 10, 23, 28, 31, 34);
UPDATE orders SET campaign_id = 3 WHERE order_id IN (5, 36, 38);
UPDATE orders SET campaign_id = 4 WHERE order_id IN (11, 25, 30, 41);
