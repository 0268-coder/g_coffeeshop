CREATE TABLE `delivery_transaction` (
  `delivery_id` int(11) NOT NULL,
  `delivery_time` datetime DEFAULT NULL,
  `transaction_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

