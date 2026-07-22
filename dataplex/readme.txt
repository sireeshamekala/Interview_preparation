Dataplex Hands on End-to-End Flow
sales.csv (Cloud Storage)
          │
          ▼
Apache Beam Dataflow Pipeline
          │
          ├── Read CSV
          ├── Parse CSV
          ├── Remove Duplicate sale_id
          ├── Remove Invalid Records
          └── Load into BigQuery
          │
          ▼
BigQuery (sales_clean)
          │
          ▼
Dataplex
    ├── Metadata Discovery
    ├── Data Profile Scan
    ├── Data Quality Scan
    ├── Data Lineage
    └── Governance
________________________________________
Step 1 - Raw Data
Your input file is
gs://dataplex-retail-demo/raw/sales.csv
This file contains the raw sales data.
Example
sale_id	customer_id	product	price	city
1	101	Laptop	80000	Hyderabad
2		  Mouse	800	Bangalore
3	103	Keyboard	-500	Pune
3	103	Keyboard	1200	Pune
________________________________________
Step 2 - Dataflow Reads the File
This line
beam.io.ReadFromText(
    "gs://dataplex-retail-demo/raw/sales.csv",
    skip_header_lines=1
)
reads the CSV file from Cloud Storage.
At this stage Dataplex is not involved.
________________________________________
Step 3 - Parse CSV
beam.ParDo(ParseCSV())
Converts each line
From
1,101,Laptop,80000,Hyderabad
To
{
 "sale_id":1,
 "customer_id":"101",
 "product":"Laptop",
 "price":80000,
 "city":"Hyderabad"
}
Still, Dataplex is not involved.
________________________________________
Step 4 - Remove Duplicate Records
You wrote
GroupByKey()
using
sale_id
Suppose the CSV contains
sale_id	customer_id
3	103
3	103
Dataflow keeps only one record.
This is your data transformation logic.
Dataplex does not remove duplicates.
________________________________________
Step 5 - Remove Invalid Records
Your code checks
customer_id == ""
and
price <= 0
If either condition is true,
the record is discarded.
Again,
This validation is performed by Dataflow, not Dataplex.
________________________________________
Step 6 - Load into BigQuery
WriteToBigQuery()
writes the cleaned data into
retail_demo.sales_clean
Now the cleaned data is stored in BigQuery.
________________________________________
Where Does Dataplex Come In?
After Dataflow finishes, Dataplex works on the BigQuery table (or another registered asset). It does not transform the data; it governs and analyzes it.
________________________________________
1. Metadata Discovery
If the BigQuery dataset is registered as a Dataplex Asset,
Dataplex automatically discovers:
•	Table name
sales_clean
•	Columns
sale_id

customer_id

product

price

city
•	Data types
INTEGER

INTEGER

STRING

FLOAT

STRING
•	Number of columns
•	Schema
•	Table information
________________________________________
2. Data Profile Scan
Suppose your cleaned table contains
100,000 rows.
Dataplex generates statistics like:
Metric	Value
Rows	100000
Columns	5
NULL customer_id	0
Duplicate sale_id	0
Minimum Price	100
Maximum Price	80000
Average Price	12500
It helps you understand the characteristics of the data.
________________________________________
3. Data Quality Scan
You can define rules such as:
•	sale_id must be unique
•	customer_id cannot be NULL
•	price > 0
Dataplex evaluates these rules on the BigQuery table and reports pass/fail results.
Example:
Rule	Status
sale_id Unique	✅ Pass
customer_id Not NULL	✅ Pass
price > 0	✅ Pass
This provides confidence that the data meets your business expectations.
________________________________________
4. Data Lineage
Dataplex can show the data flow:
Cloud Storage

sales.csv

↓

Dataflow Pipeline

↓

BigQuery

sales_clean
This helps answer questions like:
•	Where did this table come from?
•	Which pipeline produced it?
•	What was the original source?
________________________________________
5. Governance
Dataplex also provides:
•	Centralized metadata
•	Search
•	Data ownership information
•	Security integration (IAM)
•	Organization using Lakes, Zones, and Assets
________________________________________
Complete Flow
sales.csv
(Cloud Storage)

        │
        ▼

Dataflow Pipeline

        │
        ├── Read CSV
        ├── Parse CSV
        ├── Remove Duplicate sale_id
        ├── Remove Invalid Records
        └── Write to BigQuery

        ▼

BigQuery
sales_clean

        ▼

Dataplex

        ├── Metadata Discovery
        ├── Data Profile Scan
        ├── Data Quality Scan
        ├── Data Lineage
        └── Governance
What Dataplex Does Not Do
Dataplex does not:
•	Read the CSV file from GCS.
•	Parse the CSV.
•	Remove duplicate records.
•	Filter invalid rows.
•	Transform the data.
•	Load data into BigQuery.
Those tasks are handled by Dataflow (Apache Beam) in your pipeline.
What Dataplex Does Do
Once the data is available in BigQuery (or another registered asset), Dataplex helps you:
•	Discover and document the table's metadata.
•	Analyze the data with Data Profile Scans.
•	Validate business rules with Data Quality Scans.
•	Track how the data moved through the pipeline using Data Lineage.
•	Govern and organize enterprise data using Lakes, Zones, and Assets.
So, in your specific project, the responsibilities are clearly divided:
•	Dataflow = ETL (Extract, Transform, Load)
•	BigQuery = Data warehouse
•	Dataplex = Governance, quality, profiling, and lineage of the data after it has been loaded into BigQuery.


Finaloutput in bigquery table
| sale_id | customer_id | product  | price | city      |
| ------: | ----------: | -------- | ----: | --------- |
|       1 |         101 | Laptop   | 80000 | Hyderabad |
|       3 |         103 | Keyboard |  1200 | Pune      |

