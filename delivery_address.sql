CREATE TABLE `delivery_address` (
  `delivery_address_id` int(11) NOT NULL,
  `delivery_id` int(11) NOT NULL,
  `street` varchar(120) NOT NULL,
  `sub_district` varchar(100) NOT NULL,
  `district` varchar(100) NOT NULL,
  `province` varchar(100) NOT NULL,
  `postal_code` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


