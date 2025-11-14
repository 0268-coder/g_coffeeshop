CREATE TABLE `gift_card` (
  `payment_method_id` int(11) NOT NULL,
  `giftcard_id` int(11) NOT NULL,
  `initial_value` decimal(10,2) NOT NULL,
  `current_balance` decimal(10,2) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `issued_date` date NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `status` enum('Active','Used','Expired') NOT NULL DEFAULT 'Active',
  `code` varchar(20) NOT NULL,
  `purchased_by_member_id` int(11) DEFAULT NULL,
  `last_used_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DELIMITER $$
CREATE TRIGGER `trg_giftcard_increment` BEFORE INSERT ON `gift_card` FOR EACH ROW BEGIN
  DECLARE next_id INT;

SELECT IFNULL(MAX(giftcard_id), 0) + 1 INTO next_id
  FROM gift_card
  WHERE payment_method_id = NEW.payment_method_id;

SET NEW.giftcard_id = next_id;

END
$$
DELIMITER ;

