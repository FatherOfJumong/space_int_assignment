-- Scripts to create tables

-- Customers Table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(60) UNIQUE NOT NULL,
    country VARCHAR(50) NOT NULL,
    registration_date DATE DEFAULT CURRENT_DATE
) DISTRIBUTED BY (customer_id);

-- Products Table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    category VARCHAR(50) NOT NULL
) DISTRIBUTED BY (product_id);

-- Sales Transactions Table
CREATE TABLE sales_transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    purchase_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
) DISTRIBUTED BY (transaction_id)

-- Shipping Details Table
CREATE TABLE shipping_details (
    shipping_id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL REFERENCES sales_transactions(transaction_id),
    shipping_date DATE NOT NULL,
    shipping_address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL
) DISTRIBUTED BY (shipping_id);


-- Queries for analysis
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', purchase_date) AS monthz,
        SUM(pr.price * st.quantity) AS total_sales_amount,
        COUNT(st.transaction_id) AS total_transactions_count
    FROM sales_transactions st
    JOIN products pr ON st.product_id = pr.product_id
    GROUP BY monthz

)
SELECT
    monthz,
    total_sales_amount,
    total_transactions_count,
    AVG(total_sales_amount) OVER (ORDER BY monthz ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS three_month_moving_avg
FROM monthly_sales
ORDER BY monthz;