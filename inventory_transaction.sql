CREATE TABLE `inventory_transaction` (
  `movement_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `type` enum('IN','OUT') NOT NULL,
  `date` date NOT NULL,
  `transaction_id` char(36) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

