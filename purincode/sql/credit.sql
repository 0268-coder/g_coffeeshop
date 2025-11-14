CREATE TABLE `credit` (
  `payment_method_id` int(11) NOT NULL,
  `credit_id` int(11) NOT NULL,
  `last4digit` varbinary(32) NOT NULL,
  `fname` varbinary(128) NOT NULL,
  `lname` varbinary(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DELIMITER $$
CREATE TRIGGER `trg_credit_increment` BEFORE INSERT ON `credit` FOR EACH ROW BEGIN
  DECLARE next_id INT;

SELECT IFNULL(MAX(credit_id), 0) + 1 INTO next_id
  FROM credit
  WHERE payment_method_id = NEW.payment_method_id;

SET NEW.credit_id = next_id;

END
$$
DELIMITER ;

