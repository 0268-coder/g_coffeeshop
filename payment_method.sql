CREATE TABLE `payment_method` (
  `payment_method_id` int(11) NOT NULL,
  `payment_method_name` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `payment_method` (`payment_method_id`, `payment_method_name`) VALUES
(1, 'giftcard'),
(2, 'credit_card'),
(3, 'debit_card'),
(4, 'cash'),
(5, 'promptpay');
