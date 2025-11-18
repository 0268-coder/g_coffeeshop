CREATE TABLE `menu_item` (
  `menu_item_id` int(11) NOT NULL,
  `menu_item_name` varchar(100) NOT NULL,
  `menu_category` varchar(50) NOT NULL,
  `menu_price` decimal(12,2) NOT NULL,
  `menu_is_seasonal` tinyint(1) DEFAULT NULL,
  `menu_available_from` date DEFAULT NULL,
  `menu_available_to` date DEFAULT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `menu_item` (`menu_item_id`, `menu_item_name`, `menu_category`, `menu_price`, `menu_is_seasonal`, `menu_available_from`, `menu_available_to`) VALUES
(1, 'Espresso', 'coffee', '192.00', 0, NULL, NULL),
(2, 'Americano', 'coffee', '224.00', 0, NULL, NULL),
(3, 'Latte', 'coffee', '256.00', 0, NULL, NULL),
(4, 'Cappuccino', 'coffee', '256.00', 0, NULL, NULL),
(5, 'Flat White', 'coffee', '288.00', 0, NULL, NULL),
(6, 'Mocha', 'coffee', '304.00', 0, NULL, NULL),
(7, 'Hot Chocolate', 'non-coffee', '288.00', 0, NULL, NULL),
(8, 'Matcha Latte', 'non-coffee', '320.00', 0, NULL, NULL),
--new data
(9, 'Chai Latte', 'non-coffee', '192.00', 0, NULL, NULL),
(10, 'Double Espresso', 'coffee', '224.00', 0, NULL, NULL);
