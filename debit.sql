CREATE TABLE `debit` (
  `payment_method_id` int(11) NOT NULL,
  `debit_id` int(11) NOT NULL,
  `last4digit` varbinary(32) NOT NULL,
  `fname` varbinary(128) NOT NULL,
  `lname` varbinary(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DELIMITER $$
CREATE TRIGGER `trg_debit_increment` BEFORE INSERT ON `debit` FOR EACH ROW BEGIN
  DECLARE next_id INT;

SELECT IFNULL(MAX(debit_id), 0) + 1 INTO next_id
  FROM debit
  WHERE payment_method_id = NEW.payment_method_id;

SET NEW.debit_id = next_id;

END
$$
DELIMITER ;

