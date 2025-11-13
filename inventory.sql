CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `brand` varchar(60) NOT NULL,
  `category` varchar(60) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `current_stock` int(11) NOT NULL,
  `reorder_level` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

