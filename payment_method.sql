CREATE TABLE `payment_method` (
  `payment_method_id` int(11) NOT NULL,
  `payment_method_name` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `payment_method` (`payment_method_id`, `payment_method_name`) VALUES
(4, 'cash'),
(2, 'credit_card'),
(3, 'debit_card'),
(1, 'giftcard'),
(5, 'promptpay');

