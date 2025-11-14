CREATE TABLE `cash` (
  `payment_method_id` int(11) NOT NULL,
  `cash_id` int(11) NOT NULL,
  `cash_received` decimal(12,2) DEFAULT NULL,
  `cash_change` decimal(12,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DELIMITER $$
CREATE TRIGGER `trg_cash_increment` BEFORE INSERT ON `cash` FOR EACH ROW BEGIN
  DECLARE next_id INT;

SELECT IFNULL(MAX(cash_id), 0) + 1 INTO next_id
  FROM cash
  WHERE payment_method_id = NEW.payment_method_id;

SET NEW.cash_id = next_id;

END
$$
DELIMITER ;

