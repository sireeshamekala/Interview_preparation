BigQuery Partitioning
1. What is Partitioning?
Partitioning is a BigQuery feature that divides a large table into smaller logical sections called partitions based on a partition column.
Instead of scanning the entire table, BigQuery scans only the required partitions (Partition Pruning), which improves query performance and reduces query costs.
Benefits
•	Faster query execution
•	Reduces data scanned
•	Lowers query cost
•	Supports automatic deletion of old data using partition expiration
•	Improves query performance for large tables
________________________________________
2. How Partitioning Works
Suppose a table contains data for five years.
Partition	Data
Partition 1	2022
Partition 2	2023
Partition 3	2024
Partition 4	2025
Partition 5	2026
Query:
SELECT *
FROM sales
WHERE order_date = '2026-07-09';
BigQuery scans only the partition containing 2026-07-09 instead of the entire table.
This optimization is called Partition Pruning.
________________________________________
3. What is Partition Pruning?
Partition pruning is the process where BigQuery automatically skips partitions that do not match the partition filter.
For example:
•	Table contains 365 daily partitions
•	Query filters one specific date
BigQuery scans only one partition instead of all 365 partitions.
________________________________________
4. Types of Partitioning
A. Time Unit Column Partitioning (Most Common)
Uses one of the following column types:
•	DATE
•	TIMESTAMP
•	DATETIME
Example:
CREATE TABLE sales (
    order_id INT64,
    order_date DATE,
    customer STRING
)
PARTITION BY order_date;
Best for:
•	Sales
•	Orders
•	Transactions
•	Attendance
•	Healthcare records
________________________________________
B. Ingestion Time Partitioning
Partitions data automatically based on when BigQuery receives the data.
Uses:
•	_PARTITIONDATE
•	_PARTITIONTIME
Example:
CREATE TABLE logs (
    message STRING
)
PARTITION BY _PARTITIONDATE;
Best for:
•	Logs
•	Streaming data
•	Audit tables
•	IoT
________________________________________
C. Integer Range Partitioning
Uses an INT64 column.
Example:
CREATE TABLE customers (
    customer_id INT64,
    customer_name STRING
)
PARTITION BY RANGE_BUCKET(
    customer_id,
    GENERATE_ARRAY(1,10000,1000)
);
Best for:
•	Customer IDs
•	Employee IDs
•	Product IDs
•	Account Numbers
________________________________________
D. Hourly Partitioning
Supported for TIMESTAMP and DATETIME columns.
Example:
PARTITION BY TIMESTAMP_TRUNC(event_time, HOUR)
Best for:
•	IoT
•	Clickstream
•	Event data
•	Streaming applications
________________________________________
5. Creating Partitioned Tables
Create a New Table
CREATE TABLE dataset.sales (
    order_date DATE,
    customer STRING,
    amount NUMERIC
)
PARTITION BY order_date;
________________________________________
Create a Partitioned Table from an Existing Table
CREATE OR REPLACE TABLE dataset.sales_new
PARTITION BY order_date
AS
SELECT *
FROM dataset.sales_old;
________________________________________
Integer Range Partitioning
CREATE TABLE customers
PARTITION BY RANGE_BUCKET(
    customer_id,
    GENERATE_ARRAY(1,10000,1000)
)
AS
SELECT *
FROM customers_old;
________________________________________
6. Query Examples
Query Using Partition Column (Recommended)
SELECT *
FROM sales
WHERE order_date = '2026-07-09';
✅ Only the required partition is scanned.
________________________________________
Query Using a Date Range
SELECT *
FROM sales
WHERE order_date BETWEEN '2026-07-01' AND '2026-07-31';
✅ Only July partitions are scanned.
________________________________________
Query Without a Partition Filter
SELECT *
FROM sales;
❌ All partitions are scanned, increasing cost.
________________________________________
7. Partition Expiration
Automatically deletes old partitions after a specified number of days.
Example:
CREATE TABLE sales
PARTITION BY order_date
OPTIONS (
    partition_expiration_days = 180
);
Useful for:
•	Logs
•	Temporary data
•	Audit data
________________________________________
8. Require Partition Filter
Prevents users from accidentally scanning the full table.
CREATE TABLE sales
PARTITION BY order_date
OPTIONS (
    require_partition_filter = TRUE
);
Without a partition filter:
SELECT *		
FROM sales;
BigQuery returns an error.
________________________________________
9. Costs
Storage Cost
•	No additional cost for partitioning.
•	You pay only for data storage.
Query Cost
BigQuery charges based on bytes scanned.
Example:
Without Partitioning	With Partitioning
Table Size = 5 TB	Partition Size = 200 GB
Scans 5 TB	Scans 200 GB
Higher Cost	Lower Cost
________________________________________
10. Partitioning Limitations
•	Only one partition column is allowed.
•	STRING columns cannot be used for partitioning.
•	Supported partition types:
o	DATE
o	TIMESTAMP
o	DATETIME
o	INT64 (Range Partitioning)
o	Ingestion Time
•	Maximum 10,000 partitions per table.
•	You cannot directly add or change partitioning on an existing table; you must recreate the table.
•	Poor partition choices (for example, partitioning by Employee ID) can create many small partitions and reduce performance.
________________________________________
Can we change the partition column later?
No. You must recreate the table with the new partitioning scheme.
________________________________________
Partition Column Cannot Be Changed
Once a table is created, you cannot change the partition column.
If you want to partition using a different column, you must recreate the table.
________________________________________
Partitioning Does Not Reduce Storage Cost
Partitioning reduces query cost, not storage cost.
•	Storage cost remains the same. 
•	Query cost decreases because fewer bytes are scanned.
________________________________________
Partitioning on string column:
Eg: 
CREATE OR REPLACE TABLE `project_id.dataset.customer_details_partitioned`
(
    location STRING,
    address STRING,
    city STRING,
    firstname STRING,
    lastname STRING,
    loc_partition INT64
)
PARTITION BY RANGE_BUCKET(
    loc_partition,
    GENERATE_ARRAY(1, 10, 1)
)
AS
SELECT
    location,
    address,
    city,
    firstname,
    lastname,
 
    CASE
        WHEN LOWER(location) = 'bangalore' THEN 1
        WHEN LOWER(location) = 'hyderabad' THEN 2
        WHEN LOWER(location) = 'chennai' THEN 3
        WHEN LOWER(location) = 'mumbai' THEN 4
        WHEN LOWER(location) = 'delhi' THEN 5
        WHEN LOWER(location) = 'pune' THEN 6
        WHEN LOWER(location) = 'kolkata' THEN 7
        WHEN LOWER(location) = 'noida' THEN 8
        WHEN LOWER(location) = 'gurgaon' THEN 9
        ELSE 10
    END AS loc_partition
 
FROM `project_id.dataset.customer_details`;

BigQuery Clustering
1. What is Clustering?
Clustering is a BigQuery feature that organizes (sorts) data within a table or within each partition based on one or more columns.
Unlike partitioning, clustering does not create separate partitions. Instead, it stores similar values together in storage blocks, allowing BigQuery to scan fewer blocks during query execution.
Interview Definition
"Clustering organizes data in a table (or within each partition) based on selected columns. When queries filter on clustered columns, BigQuery reads only the relevant storage blocks, improving performance and reducing query costs."
________________________________________
Why is Clustering Needed?
Suppose your table contains 100 million customer records from different cities.
Customer	City
John	Hyderabad
Alice	Bangalore
Bob	Hyderabad
David	Chennai
Mike	Bangalore
Query:
SELECT *
FROM customers
WHERE city = 'Hyderabad';
Without Clustering
The records are stored randomly.
Hyderabad
Bangalore
Chennai
Hyderabad
Mumbai
Delhi
Bangalore
Hyderabad
BigQuery scans many storage blocks.
________________________________________
With Clustering
The records are stored together based on the clustered column.
Bangalore
Bangalore

Chennai

Delhi

Hyderabad
Hyderabad
Hyderabad

Mumbai
BigQuery reads only the storage blocks containing Hyderabad.
This process is called Block Pruning.
________________________________________
How Clustering Works Internally
Unlike partitioning, clustering does not create separate partitions.
Instead, BigQuery automatically sorts rows based on clustered columns.
Example
Table

Hyderabad
Delhi
Bangalore
Hyderabad
Mumbai
Delhi
After clustering
Bangalore
Bangalore

Delhi
Delhi

Hyderabad
Hyderabad

Mumbai
Now when filtering on Hyderabad, BigQuery skips unrelated storage blocks.
________________________________________
What is Block Pruning?
Block pruning is the process where BigQuery reads only the storage blocks that contain the required clustered values.
Example
Query:
SELECT *
FROM customers
WHERE city='Hyderabad';
Without clustering
Scan all storage blocks
With clustering
Scan only Hyderabad storage blocks
This reduces:
•	Query execution time
•	Bytes scanned
•	Query cost
________________________________________
Why Use Clustering?
•	Improves query performance
•	Reduces bytes scanned
•	Lowers query cost
•	Organizes data automatically
•	Works well with partitioned tables
•	No additional storage cost
________________________________________
Supported Data Types
BigQuery supports clustering on many data types, including:
•	STRING
•	INT64
•	NUMERIC
•	BOOL
•	DATE
•	DATETIME
•	TIMESTAMP
•	GEOGRAPHY
•	BIGNUMERIC
Unlike partitioning, STRING columns are supported.
________________________________________
Maximum Cluster Columns
A table can be clustered on up to 4 columns.
Example
CLUSTER BY
location,
city,
customer_type,
customer_id
BigQuery sorts data in this order:
1.	location
2.	city
3.	customer_type
4.	customer_id
________________________________________
How to Implement Clustering
Method 1 – Create a New Clustered Table
CREATE TABLE dataset.customers
(
    customer_id INT64,
    customer_name STRING,
    city STRING
)
CLUSTER BY city;
________________________________________
Method 2 – Partition + Cluster (Recommended)
CREATE TABLE dataset.orders
(
    order_date DATE,
    customer STRING,
    location STRING,
    amount NUMERIC
)
PARTITION BY order_date
CLUSTER BY location;
This is the most common production design.
________________________________________
Method 3 – Create from an Existing Table
CREATE OR REPLACE TABLE dataset.customer_new
CLUSTER BY city
AS
SELECT *
FROM dataset.customer_old;
________________________________________
Method 4 – Add Clustering to an Existing Table
If the table is not clustered, you can add clustering metadata using:
ALTER TABLE dataset.customers
SET OPTIONS (
  clustering_fields = ['city']
);
Note: BigQuery automatically reorganizes data over time through automatic reclustering. Existing rows are not instantly rewritten.
________________________________________
Query Examples
Query Using Clustered Column
SELECT *
FROM customers
WHERE city = 'Hyderabad';
BigQuery performs block pruning.
________________________________________
Query Using Multiple Cluster Columns
SELECT *
FROM customers
WHERE city = 'Hyderabad'
AND customer_type = 'Premium';
Even fewer storage blocks are read.
________________________________________
Query Without Cluster Filter
SELECT *
FROM customers;
All storage blocks are scanned.
________________________________________
Automatic Reclustering
BigQuery automatically maintains clustering as new data is inserted or updated.
You do not need to manually reorganize the data.
________________________________________
Costs
Storage Cost
No additional storage cost.
________________________________________
Query Cost
BigQuery charges based on bytes scanned.
Without clustering
Table Size

2 TB
Query scans
2 TB
With clustering
Relevant Storage Blocks

150 GB
Only 150 GB is scanned.
________________________________________
Clustering Limitations
1. Maximum Four Cluster Columns
A table can have up to four clustered columns.
________________________________________
2. Clustering Does Not Create Partitions
Clustering only organizes data inside the table (or partition).
It does not divide the table into partitions.
________________________________________
3. Benefits Depend on Query Filters
Clustering improves performance only when queries filter on clustered columns.
Example:
SELECT *
FROM customers
WHERE city = 'Hyderabad';
Good.
But:
SELECT *
FROM customers
WHERE salary > 50000;
No benefit if salary is not a clustered column.
________________________________________
4. Not Suitable for Small Tables
Small tables are scanned quickly anyway, so clustering provides little or no benefit.
________________________________________
5. Column Order Matters
For:
CLUSTER BY country, city
BigQuery organizes data by:
1.	country
2.	city
Queries filtering on country benefit the most.
Queries filtering only on city may see less benefit.
________________________________________
6. Existing Data May Not Be Immediately Reorganized
After adding clustering with ALTER TABLE, BigQuery reclusters data gradually.
________________________________________
7. Does Not Reduce Storage Cost
Like partitioning, clustering reduces query cost, not storage cost.
________________________________________
Best Practices
•	Cluster on columns frequently used in:
o	WHERE
o	JOIN
o	GROUP BY
•	Use low-to-medium cardinality columns that are commonly filtered.
•	Combine partitioning and clustering for large tables.
•	Keep the most frequently filtered column first in the CLUSTER BY list.
•	Avoid clustering very small tables.
________________________________________
Can STRING columns be clustered?
Yes. STRING is one of the most common data types used for clustering.
________________________________________
Can clustering be used without partitioning?
Yes. A table can be clustered even if it is not partitioned.

BigQuery Search Index
1. What is Search Index?
A Search Index is a BigQuery feature that creates a secondary index on one or more columns to make point lookups and text searches much faster.
Instead of scanning the entire table, BigQuery uses the search index to quickly locate the matching rows.
Unlike Partitioning, which divides a table into partitions, and Clustering, which organizes data into storage blocks, Search Index creates a separate index structure that maps searchable values to their corresponding rows.
________________________________________
Why is Search Index Needed?
Suppose you have a customer table containing 500 million records.
Customer Table
Customer ID	Customer Name	Email
1001	John	john@gmail.com

1002	Alice	alice@gmail.com

1003	Bob	john@gmail.com

1004	David	bob@gmail.com

1005	Mike	john@gmail.com

...	...	...
500,000,000	Allen	allen@gmail.com

Notice that john@gmail.com appears three times.
Suppose you execute
SELECT *
FROM customers
WHERE SEARCH(email,'john@gmail.com');
________________________________________
Without Search Index
BigQuery performs
500 Million Records
        ↓
Full Table Scan
        ↓
Returns all matching rows
It has to scan the complete table before finding every matching record.
________________________________________
With Search Index
BigQuery performs
Search Index
      ↓
john@gmail.com
      ↓
Row 1
Row 3
Row 5
      ↓
Return Results
Instead of scanning all 500 million records, BigQuery directly locates the matching rows.
Benefits
•	Faster searches
•	Less data scanned
•	Lower query cost
•	Lower query latency
________________________________________
How Search Index Works Internally
When a Search Index is created, BigQuery builds a separate index that stores:
•	Searchable values
•	References to all matching rows
________________________________________
Customer Table
Row	Customer ID	Email
1	1001	john@gmail.com

2	1002	alice@gmail.com

3	1003	john@gmail.com

4	1004	bob@gmail.com

5	1005	john@gmail.com

6	1006	alice@gmail.com

________________________________________
Search Index
Indexed Value	Row References
alice@gmail.com
Row 2, Row 6
bob@gmail.com
Row 4
john@gmail.com
Row 1, Row 3, Row 5
Notice that:
•	john@gmail.com appears three times
•	alice@gmail.com appears two times
The Search Index stores all row references, not just one.
________________________________________
Query
SELECT *
FROM customers
WHERE SEARCH(email,'john@gmail.com');
BigQuery executes
Search Index
      ↓
john@gmail.com
      ↓
Row 1
Row 3
Row 5
      ↓
Reads only these rows
      ↓
Returns Result
No full table scan occurs.
________________________________________
How Search Index Handles Duplicate Values
Search Index fully supports duplicate values.
Duplicate values are not removed.
Instead, the index stores references to every matching row.
Example
Customer Table
Customer ID	Email
1001	john@gmail.com

1002	alice@gmail.com

1003	john@gmail.com

1004	bob@gmail.com

1005	john@gmail.com

Search Index
Indexed Value	Row References
john@gmail.com
Row 1, Row 3, Row 5
alice@gmail.com
Row 2
bob@gmail.com
Row 4
When searching
SELECT *
FROM customers
WHERE SEARCH(email,'john@gmail.com');
BigQuery returns
Customer ID	Email
1001	john@gmail.com

1003	john@gmail.com

1005	john@gmail.com

Every matching row is returned.
________________________________________
Why Use Search Index?
Search Index is useful when:
•	Searching customer emails
•	Looking up usernames
•	Searching product codes
•	Searching addresses
•	Searching log messages
•	Searching JSON documents
•	Searching error messages
Benefits
•	Faster point lookups
•	Faster text searches
•	Faster JSON searches
•	Lower latency
•	Lower query cost
•	Automatically maintained by BigQuery
________________________________________
Supported Data Types
Search Index supports
•	STRING
•	JSON
It also supports searching nested fields inside JSON documents.
________________________________________
How to Implement Search Index
Method 1 – Create Search Index
CREATE SEARCH INDEX idx_customer_email
ON dataset.customers(email);
________________________________________
Method 2 – Create Search Index on JSON
CREATE SEARCH INDEX idx_payload
ON dataset.logs(payload);
________________________________________
Query Examples
Search by Email
SELECT *
FROM customers
WHERE SEARCH(email,'john@gmail.com');
Uses Search Index.
________________________________________
Search JSON
SELECT *
FROM logs
WHERE SEARCH(payload,'ERROR');
________________________________________
Search Partial Text
SELECT *
FROM customers
WHERE SEARCH(address,'Hyderabad');
Useful for searching addresses and descriptions.
________________________________________
Search Duplicate Values
SELECT *
FROM customers
WHERE SEARCH(email,'alice@gmail.com');
Result
Customer ID	Email
1002	alice@gmail.com

1006	alice@gmail.com

All matching rows are returned.
________________________________________
View Existing Search Indexes
SELECT *
FROM dataset.INFORMATION_SCHEMA.SEARCH_INDEXES;
________________________________________
Drop Search Index
DROP SEARCH INDEX idx_customer_email
ON dataset.customers;
________________________________________
Costs
Storage Cost
Unlike Partitioning and Clustering,
Search Index creates an additional index.
Therefore,
✅ Additional storage charges apply.
________________________________________
Query Cost
BigQuery charges based on bytes scanned.
Without Search Index
500 Million Records
↓
Full Table Scan

With Search Index
Search Index
↓
Matching Rows Only
Benefits
•	Less data scanned
•	Faster execution
•	Lower query cost
________________________________________
Search Index Limitations
1. Supports Only Specific Data Types
Supported
•	STRING
•	JSON
Not intended for
•	INT64
•	FLOAT64
•	DATE
•	TIMESTAMP
•	NUMERIC
________________________________________
2. Additional Storage Cost
Unlike Partitioning and Clustering,
Search Index requires additional storage because the index is stored separately.
________________________________________
3. Best for Search Queries
Search Index works best for
•	Exact matches
•	Partial text searches
•	JSON searches
It does not improve aggregation queries.
Example
SELECT COUNT(*)
FROM customers;
No Search Index benefit.
________________________________________
4. Does Not Replace Partitioning
Partitioning reduces scanned partitions.
Search Index performs fast row lookups.
They solve different problems.
________________________________________
5. Does Not Replace Clustering
Clustering organizes storage blocks.
Search Index builds a separate searchable index.
________________________________________
6. Automatic Maintenance
Whenever data changes,
BigQuery automatically updates the Search Index.
No manual maintenance is required.
________________________________________
Partitioning vs Clustering vs Search Index
Feature	Partitioning	Clustering	Search Index
Purpose	Divide table into partitions	Organize storage blocks	Create searchable index
Best For	Date filtering	Frequently filtered columns	Point lookups & text search
Optimization	Partition Pruning	Block Pruning	Index Lookup
Maximum Columns	1	4	Multiple supported columns
STRING Support	❌ No	✅ Yes	✅ Yes
Additional Storage Cost	❌ No	❌ No	✅ Yes
Duplicate Values	Supported	Supported	Supported

