BigQuery User Defined Functions (UDFs) 

1. What is a User Defined Function (UDF)?
A User Defined Function (UDF) is a custom function that you create in BigQuery to perform a specific calculation or transformation. Instead of writing the same SQL logic repeatedly, you define it once and reuse it across multiple queries.
A UDF behaves like a built-in BigQuery function (such as UPPER(), LOWER(), or ROUND()), but it contains your own business logic.
Why use UDFs?
Without a UDF, you might write the same expression in many queries.
Example:
CONCAT(first_name, ' ', last_name)
If this logic is used in 20 different queries, maintaining it becomes difficult.
Instead, create a UDF:
get_full_name(first_name, last_name)
Now, if the logic changes, you only update the function instead of every query.
________________________________________
2. Benefits of UDFs
•	Improves code readability
•	Avoids duplicate SQL logic
•	Makes SQL easier to maintain
•	Encapsulates business rules
•	Can be reused by multiple users
•	Reduces development time
________________________________________
3. Types of UDFs
BigQuery supports two types of UDFs.
3.1 SQL UDF
•	Written using SQL.
•	Best choice for most use cases.
•	Faster than JavaScript UDFs.
•	Recommended whenever SQL can solve the problem.
Example uses:
•	Discount calculations
•	Salary bands
•	String manipulation
•	Date calculations
________________________________________
3.2 JavaScript UDF
•	Written using JavaScript.
•	Used when SQL cannot implement complex logic.
•	Slightly slower because BigQuery invokes the JavaScript engine.
Example uses:
•	Complex string parsing
•	Advanced mathematical calculations
•	Custom algorithms
________________________________________
4. Types Based on Storage
BigQuery classifies UDFs into two categories.
4.1 Temporary UDF
•	Exists only for the current query.
•	Not saved inside BigQuery.
•	Automatically deleted after query execution.
•	Useful for one-time analysis.
________________________________________
4.2 Persistent UDF
•	Stored permanently inside a BigQuery dataset.
•	Can be reused in any future query.
•	Can be shared with other users having dataset permissions.
________________________________________
5. Where is a UDF Stored in BigQuery?
Temporary UDF
Temporary UDFs are not stored anywhere.
They exist only while the query executes.
Once the query finishes, BigQuery automatically removes them.
________________________________________
Persistent UDF
Persistent UDFs are stored inside a BigQuery Dataset, just like tables, views, and stored procedures.
Example hierarchy:
Project
│
├── Dataset (company_data)
│      │
│      ├── Tables
│      ├── Views
│      ├── Stored Procedures
│      └── User Defined Functions
│              │
│              ├── get_full_name
│              ├── calculate_bonus
│              └── salary_band
For example,
Project
    gcp-demo

Dataset
    hr_dataset

Function
    salary_band
Its fully qualified name becomes:
gcp-demo.hr_dataset.salary_band
________________________________________
6. How to Create a Persistent UDF
Syntax
CREATE FUNCTION project.dataset.function_name(parameter datatype)
RETURNS datatype
AS (
    SQL Expression
);
________________________________________
Example
Create a dataset if it does not already exist.
CREATE SCHEMA demo_dataset;
Now create a function.
CREATE OR REPLACE FUNCTION demo_dataset.get_full_name(
    first_name STRING,
    last_name STRING
)
RETURNS STRING
AS (
    CONCAT(first_name, ' ', last_name)
);
Function created successfully.
________________________________________
7. How to View UDFs in BigQuery UI
After creating a persistent UDF,
Open BigQuery Console
Project
    │
    └── demo_dataset
            │
            ├── Tables
            ├── Views
            ├── Functions
            │      └── get_full_name
            └── Procedures
You will find a Functions section under the dataset containing your UDFs.
________________________________________
8. How to Use a UDF
Suppose we have the following table.
employees
employee_id	first_name	last_name
101	John	Smith
102	Alice	Brown
103	David	Miller
Query
SELECT
employee_id,
first_name,
last_name,
demo_dataset.get_full_name(first_name,last_name) AS full_name
FROM employees;
Output
employee_id	full_name
101	John Smith
102	Alice Brown
103	David Miller
Notice that the UDF behaves exactly like a built-in BigQuery function.
________________________________________
9. Example 2 – Calculate Discount
Create UDF
CREATE OR REPLACE FUNCTION demo_dataset.discount_price(
price FLOAT64
)
RETURNS FLOAT64
AS (
price * 0.9
);
Sample table
Product	Price
Laptop	50000
Phone	30000
Mouse	1000
Query
SELECT
product,
price,
demo_dataset.discount_price(price) AS discounted_price
FROM products;
Output
Product	Price	Discounted Price
Laptop	50000	45000
Phone	30000	27000
Mouse	1000	900
________________________________________
10. Creating a Temporary UDF
Temporary UDFs exist only for the current query.
CREATE TEMP FUNCTION square_number(x INT64)
RETURNS INT64
AS (
x*x
);

SELECT
number,
square_number(number)
FROM UNNEST([1,2,3,4,5]) number;
Output
Number	Square
1	1
2	4
3	9
4	16
5	25
After execution completes, the function is automatically deleted.
________________________________________
11. How BigQuery Executes a UDF
When a query calls a UDF, BigQuery follows these steps:
User Query
       │
      ▼
Calls UDF
       │
      ▼
BigQuery Reads Function Definition
       │
      ▼
Applies Logic to Each Input Row
       │
      ▼
Returns Calculated Value
       │
      ▼
Final Query Output
________________________________________
12. Temporary UDF vs Persistent UDF
Feature	Temporary UDF	Persistent UDF
Stored in Dataset	❌ No	✅ Yes
Reusable	Only within the current query	Across multiple queries
Visible in UI	❌ No	✅ Yes
Automatically Deleted	✅ Yes	❌ No
Best Use Case	Ad-hoc analysis	Reusable business logic
________________________________________
13. SQL UDF vs JavaScript UDF
SQL UDF	JavaScript UDF
Written in SQL	Written in JavaScript
Faster	Slower
Recommended for most cases	Use only for complex logic
Easy to maintain	More complex to debug
________________________________________
14. Limitations
•	SQL UDFs can contain only a single SQL expression.
•	UDFs cannot execute DDL statements (CREATE, DROP, ALTER).
•	UDFs cannot execute DML statements (INSERT, UPDATE, DELETE, MERGE).
•	UDFs cannot create or modify tables.
•	JavaScript UDFs are generally slower than SQL UDFs due to JavaScript execution overhead.
________________________________________
Can a UDF be shared with other users?
Yes. A persistent UDF can be used by other users who have the necessary permissions on the dataset where it is stored.
