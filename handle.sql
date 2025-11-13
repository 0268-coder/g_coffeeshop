CREATE TABLE `handle` (
  `employee_id` int(11) NOT NULL,
  `menu_item_id` int(11) NOT NULL,
  `transaction_id` char(36) NOT NULL,
  `status` varchar(30) DEFAULT NULL,
  `handled_at` timestamp NULL DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `quantity_handled` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

