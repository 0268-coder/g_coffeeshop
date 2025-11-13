CREATE TABLE `voucher` (
  `voucher_id` int(11) NOT NULL,
  `voucher_code` varchar(30) NOT NULL,
  `voucher_discount_type` enum('fixed','percentage') NOT NULL,
  `voucher_discount_value` decimal(12,2) NOT NULL,
  `voucher_valid_from` date NOT NULL,
  `voucher_valid_to` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `voucher` (`voucher_id`, `voucher_code`, `voucher_discount_type`, `voucher_discount_value`, `voucher_valid_from`, `voucher_valid_to`) VALUES
(1, 'SALES77', 'percentage', '7.00', '2023-07-07', '2023-07-09'),
(2, 'SALES88', 'percentage', '8.00', '2023-08-08', '2023-08-10'),
(3, 'SALES99', 'percentage', '9.00', '2023-09-09', '2023-09-11'),
(4, 'SALES10', 'percentage', '10.00', '2023-10-10', '2023-10-12'),
(5, 'SALES11', 'percentage', '11.00', '2023-11-11', '2023-11-13'),
(6, 'MERDEKA', 'fixed', '160.00', '2023-08-31', '2023-09-02'),
(7, 'SALES66', 'percentage', '6.00', '2024-06-06', '2024-06-08'),
(8, 'SALES77', 'percentage', '7.00', '2024-07-07', '2024-07-09'),
(9, 'SALES88', 'percentage', '8.00', '2024-08-08', '2024-08-10'),
(10, 'SALES99', 'percentage', '9.00', '2024-09-09', '2024-09-11'),
(11, 'SALES10', 'percentage', '10.00', '2024-10-10', '2024-10-12'),
(12, 'SALES11', 'percentage', '11.00', '2024-11-11', '2024-11-13'),
(13, 'MERDEKA', 'fixed', '160.00', '2024-08-31', '2024-09-02'),
(14, 'SALES50', 'percentage', '50.00', '2024-05-01', '2024-05-01'),
(15, 'SALES66', 'percentage', '6.00', '2025-06-06', '2025-06-08'),
(16, 'SALES50', 'percentage', '50.00', '2025-05-01', '2025-05-01');

ALTER TABLE `cash`
  ADD PRIMARY KEY (`payment_method_id`,`cash_id`);

ALTER TABLE `credit`
  ADD PRIMARY KEY (`payment_method_id`,`credit_id`);

ALTER TABLE `debit`
  ADD PRIMARY KEY (`payment_method_id`,`debit_id`);

ALTER TABLE `delivery_address`
  ADD PRIMARY KEY (`delivery_address_id`,`delivery_id`),
  ADD KEY `idx_da_delivery` (`delivery_id`);

ALTER TABLE `delivery_transaction`
  ADD PRIMARY KEY (`delivery_id`),
  ADD KEY `fk_delivery_trx` (`transaction_id`);

ALTER TABLE `employee`
  ADD PRIMARY KEY (`employee_id`);

ALTER TABLE `gift_card`
  ADD PRIMARY KEY (`payment_method_id`,`giftcard_id`);

ALTER TABLE `handle`
  ADD PRIMARY KEY (`employee_id`,`menu_item_id`,`transaction_id`),
  ADD KEY `menu_item_id` (`menu_item_id`),
  ADD KEY `transaction_id` (`transaction_id`);

ALTER TABLE `inventory`
  ADD PRIMARY KEY (`inventory_id`),
  ADD UNIQUE KEY `sku` (`sku`);

ALTER TABLE `inventory_transaction`
  ADD PRIMARY KEY (`movement_id`),
  ADD KEY `fk_it_sup` (`supplier_id`),
  ADD KEY `inventory_transaction_ibfk_1` (`transaction_id`);

ALTER TABLE `menu_item`
  ADD PRIMARY KEY (`menu_item_id`);

ALTER TABLE `order_transaction`
  ADD PRIMARY KEY (`transaction_id`);

ALTER TABLE `payment_method`
  ADD PRIMARY KEY (`payment_method_id`),
  ADD UNIQUE KEY `payment_method_name` (`payment_method_name`);

ALTER TABLE `payment_transaction`
  ADD KEY `fk_pt_pm` (`payment_method_id`),
  ADD KEY `fk_pt_vc` (`voucher_id`),
  ADD KEY `payment_transaction_ibfk_1` (`transaction_id`);

ALTER TABLE `promptpay`
  ADD PRIMARY KEY (`payment_method_id`,`promptpay_id`);

ALTER TABLE `reduction`
  ADD PRIMARY KEY (`inventory_id`,`transaction_id`),
  ADD KEY `reduction_ibfk_1` (`transaction_id`);

ALTER TABLE `restock`
  ADD PRIMARY KEY (`supplier_id`,`inventory_id`),
  ADD KEY `fk_re_inv` (`inventory_id`);

ALTER TABLE `supplier`
  ADD PRIMARY KEY (`supplier_id`);

ALTER TABLE `voucher`
  ADD PRIMARY KEY (`voucher_id`),
  ADD UNIQUE KEY `uq_voucher` (`voucher_code`,`voucher_valid_from`);

ALTER TABLE `delivery_transaction`
  MODIFY `delivery_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16414;

ALTER TABLE `employee`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

ALTER TABLE `inventory_transaction`
  MODIFY `movement_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32800;

ALTER TABLE `menu_item`
  MODIFY `menu_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

ALTER TABLE `payment_method`
  MODIFY `payment_method_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `supplier`
  MODIFY `supplier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

ALTER TABLE `voucher`
  MODIFY `voucher_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

ALTER TABLE `cash`
  ADD CONSTRAINT `fk_cash_payment_method` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`payment_method_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `credit`
  ADD CONSTRAINT `credit_ibfk_1` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`payment_method_id`);

ALTER TABLE `debit`
  ADD CONSTRAINT `debit_ibfk_1` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`payment_method_id`);

ALTER TABLE `delivery_address`
  ADD CONSTRAINT `fk_da_delivery` FOREIGN KEY (`delivery_id`) REFERENCES `delivery_transaction` (`delivery_id`) ON UPDATE CASCADE;

ALTER TABLE `delivery_transaction`
  ADD CONSTRAINT `fk_delivery_trx` FOREIGN KEY (`transaction_id`) REFERENCES `order_transaction` (`transaction_id`) ON UPDATE CASCADE;

ALTER TABLE `gift_card`
  ADD CONSTRAINT `gift_card_ibfk_1` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`payment_method_id`);

ALTER TABLE `handle`
  ADD CONSTRAINT `fk_pp_pm1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `handle_ibfk_1` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item` (`menu_item_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `handle_ibfk_2` FOREIGN KEY (`transaction_id`) REFERENCES `order_transaction` (`transaction_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `inventory_transaction`
  ADD CONSTRAINT `fk_it_sup` FOREIGN KEY (`supplier_id`) REFERENCES `supplier` (`supplier_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `inventory_transaction_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `order_transaction` (`transaction_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `payment_transaction`
  ADD CONSTRAINT `fk_pt_pm` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`payment_method_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pt_vc` FOREIGN KEY (`voucher_id`) REFERENCES `voucher` (`voucher_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `payment_transaction_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `order_transaction` (`transaction_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `promptpay`
  ADD CONSTRAINT `fk_pp_pm` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`payment_method_id`) ON UPDATE CASCADE;

ALTER TABLE `reduction`
  ADD CONSTRAINT `fk_red_inv` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `reduction_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `order_transaction` (`transaction_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `restock`
  ADD CONSTRAINT `fk_re_inv` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_re_sup` FOREIGN KEY (`supplier_id`) REFERENCES `supplier` (`supplier_id`) ON UPDATE CASCADE;

COMMIT;

