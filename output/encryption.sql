-- ============================================================================
-- G_COFFEESHOP DATABASE ENCRYPTION SCRIPT
-- ============================================================================
-- This script implements AES-256 encryption for sensitive data
-- Tables affected: credit, debit, gift_card, delivery_address, employee
-- 
-- Features:
-- 1. Creates encryption key variable
-- 2. Alters table columns to VARBINARY for encrypted storage
-- 3. Encrypts all existing data
-- 4. Creates triggers for automatic encryption on INSERT/UPDATE
-- 5. Creates views for decrypted data access
-- ============================================================================

-- Set encryption key
SET @encryption_key = 'i6yPwy3Rcd2zD1eU';

-- ============================================================================
-- SECTION 1: ALTER TABLE STRUCTURES FOR ENCRYPTION
-- ============================================================================

-- Credit table: last4digit, fname, lname
ALTER TABLE `credit` 
  MODIFY COLUMN `last4digit` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `fname` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `lname` VARBINARY(256) NOT NULL;

-- Debit table: last4digit, fname, lname  
ALTER TABLE `debit`
  MODIFY COLUMN `last4digit` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `fname` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `lname` VARBINARY(256) NOT NULL;

-- Gift card table: code, purchased_by_name
ALTER TABLE `gift_card`
  MODIFY COLUMN `code` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `purchased_by_name` VARBINARY(256) DEFAULT NULL;

-- Delivery address table: street, sub_district, district, province, postal_code
ALTER TABLE `delivery_address`
  MODIFY COLUMN `street` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `sub_district` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `district` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `province` VARBINARY(256) NOT NULL,
  MODIFY COLUMN `postal_code` VARBINARY(256) NOT NULL;

-- Employee table: salary
ALTER TABLE `employee`
  MODIFY COLUMN `salary` VARBINARY(256) NOT NULL;

-- ============================================================================
-- SECTION 2: ENCRYPT EXISTING DATA
-- ============================================================================


-- Encrypt credit table data
UPDATE `credit` 
SET 
  `last4digit` = AES_ENCRYPT(`last4digit`, @encryption_key),
  `fname` = AES_ENCRYPT(`fname`, @encryption_key),
  `lname` = AES_ENCRYPT(`lname`, @encryption_key)
WHERE `last4digit` IS NOT NULL;

-- Encrypt debit table data
UPDATE `debit`
SET 
  `last4digit` = AES_ENCRYPT(`last4digit`, @encryption_key),
  `fname` = AES_ENCRYPT(`fname`, @encryption_key),
  `lname` = AES_ENCRYPT(`lname`, @encryption_key)
WHERE `last4digit` IS NOT NULL;

-- Encrypt gift_card table data
UPDATE `gift_card`
SET 
  `code` = AES_ENCRYPT(`code`, @encryption_key),
  `purchased_by_name` = CASE 
    WHEN `purchased_by_name` IS NOT NULL 
    THEN AES_ENCRYPT(`purchased_by_name`, @encryption_key)
    ELSE NULL
  END
WHERE `code` IS NOT NULL;

-- Encrypt delivery_address table data
UPDATE `delivery_address`
SET 
  `street` = AES_ENCRYPT(`street`, @encryption_key),
  `sub_district` = AES_ENCRYPT(`sub_district`, @encryption_key),
  `district` = AES_ENCRYPT(`district`, @encryption_key),
  `province` = AES_ENCRYPT(`province`, @encryption_key),
  `postal_code` = AES_ENCRYPT(`postal_code`, @encryption_key)
WHERE `street` IS NOT NULL;

-- Encrypt employee table data
UPDATE `employee`
SET 
  `salary` = AES_ENCRYPT(`salary`, @encryption_key)
WHERE `salary` IS NOT NULL;

-- ============================================================================
-- SECTION 3: CREATE ENCRYPTION TRIGGERS FOR INSERT
-- ============================================================================

-- Credit table INSERT trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_credit_encrypt_insert`$$
CREATE TRIGGER `trg_credit_encrypt_insert` 
BEFORE INSERT ON `credit` 
FOR EACH ROW 
BEGIN
  SET NEW.last4digit = AES_ENCRYPT(NEW.last4digit, @encryption_key);
  SET NEW.fname = AES_ENCRYPT(NEW.fname, @encryption_key);
  SET NEW.lname = AES_ENCRYPT(NEW.lname, @encryption_key);
END$$
DELIMITER ;

-- Debit table INSERT trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_debit_encrypt_insert`$$
CREATE TRIGGER `trg_debit_encrypt_insert` 
BEFORE INSERT ON `debit` 
FOR EACH ROW 
BEGIN
  SET NEW.last4digit = AES_ENCRYPT(NEW.last4digit, @encryption_key);
  SET NEW.fname = AES_ENCRYPT(NEW.fname, @encryption_key);
  SET NEW.lname = AES_ENCRYPT(NEW.lname, @encryption_key);
END$$
DELIMITER ;

-- Gift card table INSERT trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_gift_card_encrypt_insert`$$
CREATE TRIGGER `trg_gift_card_encrypt_insert` 
BEFORE INSERT ON `gift_card` 
FOR EACH ROW 
BEGIN
  SET NEW.code = AES_ENCRYPT(NEW.code, @encryption_key);
  IF NEW.purchased_by_name IS NOT NULL THEN
    SET NEW.purchased_by_name = AES_ENCRYPT(NEW.purchased_by_name, @encryption_key);
  END IF;
END$$
DELIMITER ;

-- Delivery address table INSERT trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_delivery_address_encrypt_insert`$$
CREATE TRIGGER `trg_delivery_address_encrypt_insert` 
BEFORE INSERT ON `delivery_address` 
FOR EACH ROW 
BEGIN
  SET NEW.street = AES_ENCRYPT(NEW.street, @encryption_key);
  SET NEW.sub_district = AES_ENCRYPT(NEW.sub_district, @encryption_key);
  SET NEW.district = AES_ENCRYPT(NEW.district, @encryption_key);
  SET NEW.province = AES_ENCRYPT(NEW.province, @encryption_key);
  SET NEW.postal_code = AES_ENCRYPT(NEW.postal_code, @encryption_key);
END$$
DELIMITER ;

-- Employee table INSERT trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_employee_encrypt_insert`$$
CREATE TRIGGER `trg_employee_encrypt_insert` 
BEFORE INSERT ON `employee` 
FOR EACH ROW 
BEGIN
  SET NEW.salary = AES_ENCRYPT(NEW.salary, @encryption_key);
END$$
DELIMITER ;

-- ============================================================================
-- SECTION 4: CREATE ENCRYPTION TRIGGERS FOR UPDATE
-- ============================================================================

-- Credit table UPDATE trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_credit_encrypt_update`$$
CREATE TRIGGER `trg_credit_encrypt_update` 
BEFORE UPDATE ON `credit` 
FOR EACH ROW 
BEGIN
  IF NEW.last4digit != OLD.last4digit THEN
    SET NEW.last4digit = AES_ENCRYPT(NEW.last4digit, @encryption_key);
  END IF;
  IF NEW.fname != OLD.fname THEN
    SET NEW.fname = AES_ENCRYPT(NEW.fname, @encryption_key);
  END IF;
  IF NEW.lname != OLD.lname THEN
    SET NEW.lname = AES_ENCRYPT(NEW.lname, @encryption_key);
  END IF;
END$$
DELIMITER ;

-- Debit table UPDATE trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_debit_encrypt_update`$$
CREATE TRIGGER `trg_debit_encrypt_update` 
BEFORE UPDATE ON `debit` 
FOR EACH ROW 
BEGIN
  IF NEW.last4digit != OLD.last4digit THEN
    SET NEW.last4digit = AES_ENCRYPT(NEW.last4digit, @encryption_key);
  END IF;
  IF NEW.fname != OLD.fname THEN
    SET NEW.fname = AES_ENCRYPT(NEW.fname, @encryption_key);
  END IF;
  IF NEW.lname != OLD.lname THEN
    SET NEW.lname = AES_ENCRYPT(NEW.lname, @encryption_key);
  END IF;
END$$
DELIMITER ;

-- Gift card table UPDATE trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_gift_card_encrypt_update`$$
CREATE TRIGGER `trg_gift_card_encrypt_update` 
BEFORE UPDATE ON `gift_card` 
FOR EACH ROW 
BEGIN
  IF NEW.code != OLD.code THEN
    SET NEW.code = AES_ENCRYPT(NEW.code, @encryption_key);
  END IF;
  IF NEW.purchased_by_name IS NOT NULL AND NEW.purchased_by_name != OLD.purchased_by_name THEN
    SET NEW.purchased_by_name = AES_ENCRYPT(NEW.purchased_by_name, @encryption_key);
  END IF;
END$$
DELIMITER ;

-- Delivery address table UPDATE trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_delivery_address_encrypt_update`$$
CREATE TRIGGER `trg_delivery_address_encrypt_update` 
BEFORE UPDATE ON `delivery_address` 
FOR EACH ROW 
BEGIN
  IF NEW.street != OLD.street THEN
    SET NEW.street = AES_ENCRYPT(NEW.street, @encryption_key);
  END IF;
  IF NEW.sub_district != OLD.sub_district THEN
    SET NEW.sub_district = AES_ENCRYPT(NEW.sub_district, @encryption_key);
  END IF;
  IF NEW.district != OLD.district THEN
    SET NEW.district = AES_ENCRYPT(NEW.district, @encryption_key);
  END IF;
  IF NEW.province != OLD.province THEN
    SET NEW.province = AES_ENCRYPT(NEW.province, @encryption_key);
  END IF;
  IF NEW.postal_code != OLD.postal_code THEN
    SET NEW.postal_code = AES_ENCRYPT(NEW.postal_code, @encryption_key);
  END IF;
END$$
DELIMITER ;

-- Employee table UPDATE trigger
DELIMITER $$
DROP TRIGGER IF EXISTS `trg_employee_encrypt_update`$$
CREATE TRIGGER `trg_employee_encrypt_update` 
BEFORE UPDATE ON `employee` 
FOR EACH ROW 
BEGIN
  IF NEW.salary != OLD.salary THEN
    SET NEW.salary = AES_ENCRYPT(NEW.salary, @encryption_key);
  END IF;
END$$
DELIMITER ;

-- ============================================================================
-- SECTION 5: CREATE DECRYPTION FUNCTION
-- ============================================================================
-- Note: MySQL views cannot contain variables, so we create a function
-- that uses a hardcoded key. In production, consider using MySQL's
-- keyring plugin or external key management.

DELIMITER $$
DROP FUNCTION IF EXISTS `decrypt_data`$$
CREATE FUNCTION `decrypt_data`(encrypted_data VARBINARY(256))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
  -- IMPORTANT: Change this key to match your encryption key
  DECLARE decryption_key VARCHAR(255) DEFAULT 'i6yPwy3Rcd2zD1eU';
  RETURN CAST(AES_DECRYPT(encrypted_data, decryption_key) AS CHAR);
END$$
DELIMITER ;

-- ============================================================================
-- SECTION 6: CREATE DECRYPTED VIEWS
-- ============================================================================

-- Credit table decrypted view
DROP VIEW IF EXISTS `vw_credit_decrypted`;
CREATE VIEW `vw_credit_decrypted` AS
SELECT 
  `payment_method_id`,
  `credit_id`,
  decrypt_data(`last4digit`) AS `last4digit`,
  decrypt_data(`fname`) AS `fname`,
  decrypt_data(`lname`) AS `lname`
FROM `credit`;

-- Debit table decrypted view
DROP VIEW IF EXISTS `vw_debit_decrypted`;
CREATE VIEW `vw_debit_decrypted` AS
SELECT 
  `payment_method_id`,
  `debit_id`,
  decrypt_data(`last4digit`) AS `last4digit`,
  decrypt_data(`fname`) AS `fname`,
  decrypt_data(`lname`) AS `lname`
FROM `debit`;

-- Gift card table decrypted view
DROP VIEW IF EXISTS `vw_gift_card_decrypted`;
CREATE VIEW `vw_gift_card_decrypted` AS
SELECT 
  `payment_method_id`,
  `giftcard_id`,
  `initial_value`,
  `current_balance`,
  `title`,
  `issued_date`,
  `expiry_date`,
  `status`,
  decrypt_data(`code`) AS `code`,
  CASE 
    WHEN `purchased_by_name` IS NOT NULL 
    THEN decrypt_data(`purchased_by_name`)
    ELSE NULL
  END AS `purchased_by_name`,
  `last_used_date`
FROM `gift_card`;

-- Delivery address table decrypted view
DROP VIEW IF EXISTS `vw_delivery_address_decrypted`;
CREATE VIEW `vw_delivery_address_decrypted` AS
SELECT 
  `delivery_address_id`,
  `delivery_id`,
  decrypt_data(`street`) AS `street`,
  decrypt_data(`sub_district`) AS `sub_district`,
  decrypt_data(`district`) AS `district`,
  decrypt_data(`province`) AS `province`,
  decrypt_data(`postal_code`) AS `postal_code`
FROM `delivery_address`;

-- Employee table decrypted view
DROP VIEW IF EXISTS `vw_employee_decrypted`;
CREATE VIEW `vw_employee_decrypted` AS
SELECT 
  `employee_id`,
  `name`,
  `position`,
  `hire_date`,
  CAST(decrypt_data(`salary`) AS DECIMAL(12,2)) AS `salary`
FROM `employee`;

-- ============================================================================
-- SECTION 7: GRANT PERMISSIONS (OPTIONAL - ADJUST AS NEEDED)
-- ============================================================================

-- Example: Grant SELECT on decrypted views to authorized users only
-- GRANT SELECT ON `vw_credit_decrypted` TO 'admin_user'@'localhost';
-- GRANT SELECT ON `vw_debit_decrypted` TO 'admin_user'@'localhost';
-- GRANT SELECT ON `vw_gift_card_decrypted` TO 'admin_user'@'localhost';
-- GRANT SELECT ON `vw_delivery_address_decrypted` TO 'admin_user'@'localhost';
-- GRANT SELECT ON `vw_employee_decrypted` TO 'hr_user'@'localhost';
-- GRANT EXECUTE ON FUNCTION `decrypt_data` TO 'admin_user'@'localhost';

-- ============================================================================
-- ENCRYPTION IMPLEMENTATION COMPLETED
-- ============================================================================
-- 
-- USAGE NOTES:
-- 
-- 1. SECURITY: The encryption key is stored in TWO places - update BOTH:
--    - Line 17: SET @encryption_key (for initial data encryption & triggers)
--    - decrypt_data function: decryption_key variable (for views)
--    Both MUST match! In production, use MySQL keyring or external key mgmt.
-- 
-- 2. INSERTING DATA: Insert plain text data - triggers will auto-encrypt
--    Example: INSERT INTO credit VALUES (1, 1, '1234', 'John', 'Doe');
-- 
-- 3. VIEWING DECRYPTED DATA: Query the views instead of base tables
--    Example: SELECT * FROM vw_credit_decrypted;
-- 
-- 4. UPDATING DATA: Update with plain text - triggers will auto-encrypt
--    Example: UPDATE credit SET fname = 'Jane' WHERE credit_id = 1;
-- 
-- 5. DIRECT DECRYPTION: You can also use the decrypt_data function directly
--    Example: SELECT payment_method_id, decrypt_data(fname) FROM credit;
-- 
-- 6. BACKUP: Ensure encryption key is backed up separately from database
-- 
-- 7. PERFORMANCE: Encryption/decryption adds overhead - monitor queries
--    Consider indexing on encrypted columns if searching is needed
-- 
-- 8. KEY ROTATION: To rotate keys:
--    a) Update @encryption_key and decrypt_data function with new key
--    b) Decrypt all data with old key and re-encrypt with new key
--    c) Drop and recreate triggers with new key reference
-- 
-- ============================================================================