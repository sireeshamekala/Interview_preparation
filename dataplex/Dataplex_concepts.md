1. What is Google Cloud Dataplex?
Google Cloud Dataplex is a fully managed data governance and data management service in Google Cloud Platform (GCP).
It helps organizations organize, discover, monitor, govern, and secure data stored in different Google Cloud services.
Dataplex does not store data.
Instead, it manages data that is already stored in:
•	Cloud Storage (GCS)
•	BigQuery
•	BigLake
Think of Dataplex as a manager for all your enterprise data.
________________________________________
2. Why Do We Need Dataplex?
Imagine a company has:
•	100 Cloud Storage buckets
•	500 BigQuery datasets
•	Thousands of BigQuery tables
Different teams create data every day.
Problems without Dataplex:
•	Difficult to find datasets
•	Duplicate datasets
•	Poor data quality
•	No ownership information
•	No data lineage
•	Difficult to search data
•	No centralized governance
Dataplex solves all these problems by providing one centralized platform.
________________________________________
3. What Does Dataplex Do?
Dataplex provides the following features:
•	Metadata Discovery
•	Data Profiling
•	Data Quality Validation
•	Data Lineage
•	Enterprise Search
•	Data Governance
•	IAM Integration
•	Centralized Data Management
________________________________________
4. Dataplex Architecture
                    Users
                      │
                      ▼
               Google Dataplex
                      │
        ┌─────────────┼──────────────┐
        ▼                        ▼                                 ▼
 Metadata       Data Quality     Lineage
 Governance      Search
                      │
                      ▼
     Cloud Storage   BigQuery   BigLake
Important:
Dataplex does not store business data.
Business data remains in:
•	Cloud Storage
•	BigQuery
•	BigLake
Dataplex only manages and governs the data.
________________________________________
5. Core Components of Dataplex
Dataplex is built using three components:
•	Lake
•	Zone
•	Asset
________________________________________
5.1 Lake
A Lake is the highest-level container in Dataplex.
It represents a business domain.
Examples:
•	Retail Lake
•	Banking Lake
•	Finance Lake
•	Healthcare Lake
Think of a Lake like the main folder.
Example:
Retail Lake
________________________________________
5.2 Zone
A Zone is created inside a Lake.
Zones organize data based on its lifecycle.
Common Zone Types:
•	Raw Zone
•	Curated Zone
•	Analytics Zone
•	Sensitive Zone
Example:
Retail Lake

│
├── Raw Zone
├── Curated Zone
├── Analytics Zone
|─ Sensitive Zone
________________________________________
5.3 Asset
Assets are the actual data resources managed by Dataplex.
Assets can be:
•	Cloud Storage Bucket
•	BigQuery Dataset
•	BigLake Tables
Example:
gs://sales-data

BigQuery Dataset
sales_dataset
________________________________________
6. Understanding Zones
Raw Zone
Stores raw data.
Example:
sales.csv
customer.csv
inventory.csv
Characteristics:
•	Original data
•	Duplicates allowed
•	NULL values allowed
•	No validation
________________________________________
Curated Zone
Stores cleaned data.
Example:
sales_clean

customer_clean
Characteristics:
•	Duplicates removed
•	Invalid rows removed
•	Validated data
________________________________________
Analytics Zone
Contains reporting tables.
Example:
daily_sales

monthly_sales

customer_summary
Business users use these tables.
________________________________________
Sensitive Zone
Contains confidential information.
Examples:
•	Salary
•	PAN Number
•	Aadhaar Number
•	Credit Card Details
Only authorized users should access this data.
________________________________________
7. Metadata Discovery
Metadata means:
Data about Data
Example:
Actual Data
Sale_ID	Customer	Amount
101	John	500
Metadata
•	Table Name
•	Column Names
•	Data Types
•	Number of Rows
•	Schema
When an Asset is registered,
Dataplex automatically discovers metadata.
________________________________________
8. Data Profile Scan
A Data Profile Scan analyzes the dataset and generates statistics.
Example:
Metric	Value
Rows	50,000
Columns	12
NULL Values	120
Duplicate Records	15
Minimum Price	100
Maximum Price	250000
Purpose:
Understand the data before using it.
________________________________________
9. Data Quality Scan
A Data Quality Scan validates the dataset using business rules.
Example Rules:
•	Customer ID should not be NULL
•	Sale ID should be unique
•	Price should be greater than zero
Example Dataset
Sale_ID	Customer	Price
101	John	1000
102		2000
102	David	2000
103	Alice	-100
Results
Rule	Status
Unique Sale_ID	❌ Failed
Customer Not NULL	❌ Failed
Price > 0	❌ Failed
Purpose:
Ensure only good quality data is used.
________________________________________
10. Difference Between Profile Scan and Quality Scan
Data Profile Scan	Data Quality Scan
Analyzes data	Validates data
Generates statistics	Checks business rules
No Pass/Fail	Pass/Fail Result
Used before Quality Scan	Used after Profile Scan
________________________________________
11. Data Lineage
Data Lineage shows how data moves from source to destination.
Example
Cloud Storage

sales.csv

↓

Dataflow

↓

BigQuery

sales_clean

↓

Looker Dashboard
Benefits:
•	Know where data came from
•	Debug pipelines easily
•	Root Cause Analysis
•	Impact Analysis
________________________________________
12. Data Governance
Data Governance means managing enterprise data properly.
Goals:
•	Correct data
•	Secure data
•	Trusted data
•	Standardized data
Dataplex helps governance using:
•	Lakes
•	Zones
•	Metadata
•	Quality
•	Lineage
•	IAM
________________________________________
13. Enterprise Search
Instead of manually searching datasets,
Search:
sales
Dataplex returns:
•	Sales Dataset
•	Sales Bucket
•	Metadata
•	Owner
•	Schema
•	Quality Status
________________________________________
14. Dataplex Integration with GCP Services
Cloud Storage
Stores raw files.
Example
sales.csv
Registered as an Asset.
________________________________________
BigQuery
Stores processed data.
Dataplex performs:
•	Metadata Discovery
•	Profile Scan
•	Quality Scan
•	Lineage
________________________________________
Dataflow
Processes data.
Example:
Read CSV

↓

Remove Duplicates

↓

Remove Invalid Rows

↓

Load to BigQuery
Dataplex captures metadata and lineage.
________________________________________
Cloud Composer (Airflow)
Composer orchestrates the pipeline.
Example:
GCS Sensor

↓

Run Dataflow

↓

Run Data Profile Scan

↓

Run Data Quality Scan

↓

Send Notification
________________________________________
15. End-to-End Project Flow
Source System

↓

Cloud Storage

↓

Cloud Composer DAG

↓

Dataflow Pipeline

↓

BigQuery

↓

Dataplex

     ├── Metadata Discovery

     ├── Data Profile Scan

     ├── Data Quality Scan

     ├── Data Lineage

     └── Search

↓

Business Dashboard
________________________________________
16. Can We Run Dataplex Scans from Airflow?
Yes.
There is currently no dedicated Airflow operator for Dataplex Data Scans.
We can use:
•	PythonOperator
•	Dataplex Python Client (google-cloud-dataplex)
Workflow:
PythonOperator

↓

Create Scan

↓

Run Scan

↓

Wait for Completion

↓

Read Results

↓

Fail DAG if Quality Rules Fail
________________________________________
17. Real-Time Example
Suppose every day:
A new file
sales.csv
is uploaded to Cloud Storage.
Pipeline:
Cloud Storage

↓

Composer DAG Starts

↓

Dataflow Cleans Data

↓

BigQuery Stores Data

↓

Dataplex Runs Profile Scan

↓

Dataplex Runs Quality Scan

↓

Business Users Query Data
Now the company knows:
•	Where the data came from
•	Whether the data is clean
•	Who owns it
•	Which pipeline created it
•	Whether it can be trusted
________________________________________
📘 Google Cloud Dataplex – Complete Learning & Hands-on Guide
This is the most important section because it shows what you actually did.
For every step, write:
Step 1 – Enable APIs
Services enabled:
•	Dataplex API
•	BigQuery API
•	Cloud Storage API
•	Dataflow API
•	Cloud Composer API
Why?
Dataplex requires these services to discover data, run scans, and integrate with other GCP services.
________________________________________
Step 2 – Create Cloud Storage Bucket
Bucket Name
dataplex-demo-bucket
Created folders
raw/

processed/

archive/
Uploaded
sales.csv
Why?
Cloud Storage stores the incoming raw files.
________________________________________
Step 3 – Create BigQuery Dataset
Dataset
retail_demo
Table
sales_clean
Why?
BigQuery stores cleaned and processed data.
________________________________________
Step 4 – Create Dataplex Lake
Lake Name
Retail Lake
Purpose
Represents the Retail business domain.
________________________________________
Step 5 – Create Zones
Created
Raw Zone

Curated Zone
Purpose
Raw Zone
Stores raw data.
Curated Zone
Stores cleaned data.
________________________________________
Step 6 – Register Assets
Registered
Cloud Storage Bucket
gs://dataplex-demo-bucket
Registered
BigQuery Dataset
retail_demo
Purpose
Allows Dataplex to manage these resources.
________________________________________
Step 7 – Run Metadata Discovery
Dataplex automatically discovered
•	Table Schema
•	Columns
•	Data Types
Observed
Metadata appeared in Dataplex.
________________________________________
Step 8 – Run Profile Scan
Scan Name
Sales Profile Scan
Results
Observed
•	NULL Count
•	Duplicate Count
•	Min Value
•	Max Value
•	Average
•	Data Distribution
________________________________________
Step 9 – Run Data Quality Scan
Created Rules
Customer_ID
Not NULL
Sale_ID
Unique
Price
Greater than zero
Observed
Pass/Fail status for each rule.
________________________________________
Step 10 – Verify Lineage
Observed
Cloud Storage

↓

Dataflow

↓

BigQuery
Dataplex automatically showed the relationship.
________________________________________
Step 11 – Integration with Composer
Created Airflow DAG.
Workflow
GCS Sensor

↓

Dataflow Job

↓

Profile Scan

↓

Quality Scan

↓

Read Results
Used
PythonOperator
Reason
No dedicated Dataplex Airflow operator is currently available.
