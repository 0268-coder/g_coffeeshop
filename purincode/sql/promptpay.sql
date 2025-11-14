CREATE TABLE `promptpay` (
  `payment_method_id` int(11) NOT NULL,
  `promptpay_id` varchar(40) NOT NULL,
  `transaction_ref` varchar(60) DEFAULT NULL,
  `bank_name` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

