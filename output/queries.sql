/* ============================================================================
   Consolidated SQL Queries
   Extracted from CSS325_sec3_gr4_report1_ID368_175_223_268_335_372.pdf
   ============================================================================ */


/* ============================================================================
   Query No.1
   Owner: 6622770335, Napat Hirunsak
   Objective: Analyze orders with delivery address & payment method.
============================================================================ */

SELECT
    ot.transaction_id,
    ot.order_created_at,
    dt.delivery_time,
    da.street,
    da.sub_district,
    da.district,
    da.province,
    pm.payment_method_name
FROM order_transaction AS ot
JOIN delivery_transaction AS dt  ON ot.transaction_id = dt.transaction_id
JOIN delivery_address     AS da  ON dt.delivery_id    = da.delivery_id
JOIN payment_transaction  AS pt  ON ot.transaction_id = pt.transaction_id
JOIN payment_method       AS pm  ON pt.payment_method_id = pm.payment_method_id
ORDER BY ot.order_created_at;



/* ============================================================================
   Query No.2
   Owner: 6622770335, Napat Hirunsak
   Objective: Daily inventory movement per SKU (IN, OUT, NET).
============================================================================ */

WITH daily_move AS (
    SELECT
        it.`date`,
        it.supplier_id,
        it.transaction_id,
        it.type,
        it.quantity,
        COALESCE(r.inventory_id, rs.inventory_id) AS inventory_id
    FROM inventory_transaction it
    LEFT JOIN reduction r ON r.transaction_id = it.transaction_id
    LEFT JOIN restock rs  ON rs.supplier_id = it.supplier_id
)
SELECT
    dm.`date`,
    i.sku,
    i.item_name,
    SUM(CASE WHEN dm.type = 'IN'  THEN dm.quantity ELSE 0 END) AS qty_in,
    SUM(CASE WHEN dm.type = 'OUT' THEN dm.quantity ELSE 0 END) AS qty_out,
    SUM(CASE WHEN dm.type = 'IN'  THEN dm.quantity ELSE -dm.quantity END) AS net_qty
FROM daily_move dm
LEFT JOIN inventory i ON i.inventory_id = dm.inventory_id
GROUP BY dm.`date`, i.sku, i.item_name
ORDER BY dm.`date`, i.sku;



/* ============================================================================
   Query No.3
   Owner: 6622770335, Napat Hirunsak
   Objective: Count transactions per payment method.
============================================================================ */

SELECT 
    payment_method_id,
    COUNT(transaction_id) AS usage_count
FROM payment_transaction
GROUP BY payment_method_id;



/* ============================================================================
   Query No.4
   Owner: 6622770335, Napat Hirunsak
   Objective: Employee tenure in days.
============================================================================ */

SELECT
    name,
    position,
    hire_date,
    DATEDIFF(CURDATE(), hire_date) AS days_employed
FROM employee
ORDER BY days_employed DESC;



/* ============================================================================
   Query No.5
   Owner: 6622782223, Chaiyapat Anantarasuchart
   Objective: Hourly revenue for a specific date.
============================================================================ */

SELECT 
    DATE(payment_created_at) AS pay_date,
    HOUR(payment_created_at) AS hour,
    SUM(payment_final_amount) AS hourly_revenue
FROM payment_transaction
WHERE DATE(payment_created_at) IN ('2025-06-01')
GROUP BY DATE(payment_created_at), HOUR(payment_created_at)
ORDER BY pay_date, hour;



/* ============================================================================
   Query No.6
   Owner: 6622782223, Chaiyapat Anantarasuchart
   Objective: Item with lowest stock.
============================================================================ */

SELECT
    inventory_id,
    item_name,
    current_stock
FROM inventory
ORDER BY current_stock ASC
LIMIT 1;



/* ============================================================================
   Query No.7
   Owner: 6622782223, Chaiyapat Anantarasuchart
   Objective: Delivery count by district.
============================================================================ */

SELECT 
    da.district,
    COUNT(*) AS delivery_count
FROM delivery_transaction d
JOIN vw_delivery_address_decrypted da 
    ON d.delivery_id = da.delivery_id
GROUP BY da.district
ORDER BY delivery_count DESC;



/* ============================================================================
   Query No.8
   Owner: 6622782223, Chaiyapat Anantarasuchart
   Objective: Top-selling menu item per hour.
============================================================================ */

SELECT 
    t.hour,
    t.menu_name,
    t.total_sold
FROM (
    SELECT
        HOUR(ot.order_created_at) AS hour,
        m.menu_item_name AS menu_name,
        COUNT(*) AS total_sold
    FROM order_transaction ot
    JOIN handle h ON ot.transaction_id = h.transaction_id
    JOIN menu_item m ON h.menu_item_id = m.menu_item_id
    GROUP BY HOUR(ot.order_created_at), m.menu_item_name
) AS t
JOIN (
    SELECT 
        hour,
        MAX(total_sold) AS max_sold
    FROM (
        SELECT
            HOUR(ot.order_created_at) AS hour,
            m.menu_item_name AS menu_name,
            COUNT(*) AS total_sold
        FROM order_transaction ot
        JOIN handle h ON ot.transaction_id = h.transaction_id
        JOIN menu_item m ON h.menu_item_id = m.menu_item_id
        GROUP BY HOUR(ot.order_created_at), m.menu_item_name
    ) AS x
    GROUP BY hour
) AS mx
ON  t.hour       = mx.hour
AND t.total_sold = mx.max_sold
ORDER BY t.hour;



/* ============================================================================
   Query No.9
   Owner: 6622770368, Purin Kanjanakumnerd
   Objective: Cash summary (received, change, avg actual payment).
============================================================================ */

SELECT 
    COUNT(*) AS total_transactions,
    SUM(cash_received) AS total_cash_received,
    SUM(cash_change) AS total_cash_change,
    ROUND(AVG(cash_received - cash_change), 2) AS avg_actual_payment
FROM cash;



/* ============================================================================
   Query No.10
   Owner: 6622770368, Purin Kanjanakumnerd
   Objective: Avg qty handled per employee.
============================================================================ */

SELECT 
    employee_id, 
    AVG(quantity_handled) AS avg_qty
FROM handle
GROUP BY employee_id
ORDER BY avg_qty DESC;



/* ============================================================================
   Query No.11
   Owner: 6622770368, Purin Kanjanakumnerd
   Objective: Menu popularity × payment method revenue.
============================================================================ */

SELECT
    m.menu_item_name,
    pm.payment_method_name,
    COUNT(DISTINCT p.transaction_id) AS total_orders,
    ROUND(SUM(p.payment_final_amount), 2) AS total_revenue
FROM payment_transaction p
JOIN payment_method pm ON p.payment_method_id = pm.payment_method_id
JOIN order_transaction o ON p.transaction_id = o.transaction_id
JOIN menu_item m ON o.order_unit_price = m.menu_price
GROUP BY m.menu_item_name, pm.payment_method_name
ORDER BY total_revenue DESC, total_orders DESC;



/* ============================================================================
   Query No.12
   Owner: 6622770368, Purin Kanjanakumnerd
   Objective: Hourly sales distribution across all days.
============================================================================ */

SELECT
    HOUR(p.payment_created_at) AS hour_of_day,
    COUNT(DISTINCT p.transaction_id) AS total_orders,
    ROUND(SUM(p.payment_final_amount), 2) AS total_revenue,
    ROUND(AVG(p.payment_final_amount), 2) AS avg_order_value
FROM payment_transaction p
GROUP BY HOUR(p.payment_created_at)
ORDER BY hour_of_day;



/* ============================================================================
   Query No.13
   Owner: 6622772372, Pannawat Thawonwong
   Objective: Employee count by position.
============================================================================ */

SELECT 
    position,
    COUNT(*) AS total_staff
FROM employee
GROUP BY position
ORDER BY total_staff DESC;



/* ============================================================================
   Query No.14
   Owner: 6622772372, Pannawat Thawonwong
   Objective: Average menu price per category.
============================================================================ */

SELECT
    menu_category,
    ROUND(AVG(menu_price), 2) AS avg_price,
    MIN(menu_price) AS min_price,
    MAX(menu_price) AS max_price
FROM menu_item
GROUP BY menu_category
ORDER BY avg_price DESC;



/* ============================================================================
   Query No.15
   Owner: 6622772372, Pannawat Thawonwong
   Objective: Employee contribution to sales.
============================================================================ */

SELECT 
    e.employee_id,
    e.name,
    e.position,
    ROUND(SUM(h.quantity_handled * mi.menu_price), 2) AS total_sales_contributed
FROM handle h
JOIN employee e ON e.employee_id = h.employee_id
JOIN menu_item mi ON mi.menu_item_id = h.menu_item_id
GROUP BY e.employee_id, e.name, e.position
ORDER BY total_sales_contributed DESC;



/* ============================================================================
   Query No.16
   Owner: 6622772372, Pannawat Thawonwong
   Objective: Revenue by PromptPay bank.
============================================================================ */

SELECT 
    pp.bank_name,
    COUNT(*) AS txn,
    ROUND(SUM(pt.payment_final_amount), 2) AS revenue
FROM payment_transaction pt
JOIN payment_method pm ON pm.payment_method_id = pt.payment_method_id
JOIN promptpay pp ON pp.payment_method_id = pm.payment_method_id
WHERE pm.payment_method_name LIKE 'PromptPay%'
GROUP BY pp.bank_name
ORDER BY revenue DESC;



/* ============================================================================
   Query No.17
   Owner: 6622780268, Ratchanon Wongwitutai
   Objective: Count orders grouped by handle status.
============================================================================ */

SELECT
    status,
    COUNT(DISTINCT transaction_id) AS orders
FROM handle
GROUP BY status;



/* ============================================================================
   Query No.18
   Owner: 6622780268, Ratchanon Wongwitutai
   Objective: Average stock per category.
============================================================================ */

SELECT 
    category, 
    AVG(current_stock) AS avg_stock
FROM inventory
GROUP BY category;



/* ============================================================================
   Query No.19
   Owner: 6622780268, Ratchanon Wongwitutai
   Objective: Supplier → total incoming quantity.
============================================================================ */

SELECT 
    s.supplier_name,
    SUM(CASE WHEN it.type = 'IN' THEN it.quantity ELSE 0 END) AS total_in_qty
FROM inventory_transaction it
JOIN supplier s ON it.supplier_id = s.supplier_id
GROUP BY s.supplier_name
ORDER BY total_in_qty DESC;



/* ============================================================================
   Query No.20
   Owner: 6622780268, Ratchanon Wongwitutai
   Objective: Avg handling time per status.
============================================================================ */

SELECT 
    h.status,
    ROUND(AVG(ABS(TIMESTAMPDIFF(MINUTE, ot.order_created_at, h.handled_at))), 2)
        AS avg_handling_minutes
FROM handle h
JOIN order_transaction ot ON h.transaction_id = ot.transaction_id
WHERE h.handled_at IS NOT NULL
GROUP BY h.status
ORDER BY avg_handling_minutes DESC;



/* ============================================================================
   Query No.21
   Owner: 6622781175, Tagrid Chongkolrattanapond
   Objective: Count orders handled today.
============================================================================ */

SELECT
    COUNT(DISTINCT h.transaction_id) AS orders_handled_today
FROM handle h
WHERE DATE(h.handled_at) = CURDATE();



/* ============================================================================
   Query No.22
   Owner: 6622781175, Tagrid Chongkolrattanapond
   Objective: Payment method usage frequency & revenue.
============================================================================ */

SELECT
    pm.payment_method_name,
    COUNT(*) AS payments,
    SUM(pt.payment_final_amount) AS total_amount
FROM payment_transaction pt
JOIN payment_method pm ON pm.payment_method_id = pt.payment_method_id
GROUP BY pm.payment_method_name
ORDER BY total_amount DESC;



/* ============================================================================
   Query No.23
   Owner: 6622781175, Tagrid Chongkolrattanapond
   Objective: District-based payment and revenue breakdown.
============================================================================ */

SELECT
    da.district,
    COUNT(DISTINCT ot.transaction_id) AS total_orders_in_district,
    ROUND(SUM(pt.payment_final_amount), 2) AS total_revenue_in_district,
    SUM(CASE WHEN pm.payment_method_name = 'cash' THEN 1 ELSE 0 END) AS cash_txns,
    SUM(CASE WHEN pm.payment_method_name = 'promptpay' THEN 1 ELSE 0 END) AS promptpay_txns,
    SUM(CASE WHEN pm.payment_method_name IN ('credit', 'debit') THEN 1 ELSE 0 END) AS card_txns,
    ROUND(
        SUM(CASE WHEN pm.payment_method_name = 'cash' THEN 1 ELSE 0 END) 
        * 100.0 / COUNT(DISTINCT ot.transaction_id), 
        2
    ) AS cash_pct
FROM order_transaction ot
JOIN delivery_transaction dt ON ot.transaction_id = dt.transaction_id
JOIN delivery_address da ON dt.delivery_id = da.delivery_id
JOIN payment_transaction pt ON ot.transaction_id = pt.transaction_id
JOIN payment_method pm ON pt.payment_method_id = pm.payment_method_id
GROUP BY da.district
ORDER BY total_revenue_in_district DESC;



/* ============================================================================
   Query No.24
   Owner: 6622781175, Tagrid Chongkolrattanapond
   Objective: Daily sales performance summary.
============================================================================ */

SELECT
    DATE(payment_created_at) AS sale_date,
    COUNT(DISTINCT transaction_id) AS total_orders,
    ROUND(SUM(payment_final_amount), 2) AS total_daily_revenue
FROM payment_transaction
GROUP BY DATE(payment_created_at)
ORDER BY sale_date DESC;

