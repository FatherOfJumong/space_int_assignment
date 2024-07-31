# Python Assignment

This project is an assignment for Space International. It processes contract data, generates features, and saves the results.

## Project Structure

- `main.py`: Main script to run the project
- `src/feature_generation.py`: Contains functions for feature generation
- `utils.py`: Utility functions for data processing
- `data/`: Directory containing input and output data files

## Features Generated

1. `tot_claim_cnt_l180d`: Number of claims in the last 180 days
2. `disb_bank_loan_wo_tbc`: Sum of exposure of loans without TBC and other specified banks
3. `day_sinlastloan`: Number of days since the last loan
4. `avg_loan_amnt`: Average loan amount for the client
5. `loan_frequency`: Loan frequency (loans per year) for the client

## Linters used to beautify the code
- pylint==3.2.6
- flake8==7.1.0

# SQL Assignment

This project includes a SQL assignment focusing on data analysis in a Greenplum database environment. The assignment involves:

1. Creating tables for customers, products, sales transactions, and shipping details.
2. Writing SQL queries to analyze sales data, including:
   - Calculating total sales amount and transaction count per month
   - Computing a 3-month moving average of sales

The SQL script `script.sql` contains both the table creation statements and the analysis query.

Key components of the script:
- Table creation for customers, products, sales_transactions, and shipping_details
- A complex query using Common Table Expressions (CTE) and window functions to calculate:
  - Monthly total sales amount
  - Monthly transaction count
  - 3-month moving average of sales
