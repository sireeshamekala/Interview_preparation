Niko Health - Event Driven Data Pipeline using GCP
Project Overview
This project demonstrates an end-to-end event-driven data pipeline on Google Cloud Platform (GCP). Whenever a CSV file is uploaded into a Cloud Storage bucket, the pipeline automatically triggers data processing and loads the cleaned data into BigQuery.
________________________________________
Architecture
Cloud Storage
      │
      ▼
Eventarc
      │
      ▼
Cloud Run Function
      │
      ▼
Cloud Composer (Airflow)
      │
      ▼
Dataproc Serverless (PySpark)
      │
      ▼
BigQuery
________________________________________
Services Used
•	Google Cloud Storage (GCS)
•	Eventarc
•	Cloud Run Functions
•	Cloud Composer (Apache Airflow)
•	Dataproc Serverless
•	BigQuery
________________________________________
Bucket Structure
gs://niko-health/

employee/
student/
spark-code/
    └── Niko_Health_dataproc.py
Temporary Bucket
gs://niko-health-temp
________________________________________
Workflow
Step 1
Upload a CSV file into
gs://niko-health/employee/
________________________________________
Step 2
Cloud Storage generates an Object Finalized event.
________________________________________
Step 3
Eventarc listens for the event and triggers the Cloud Run Function.
________________________________________
Step 4
Cloud Run Function
•	Reads bucket name
•	Reads uploaded file name
•	Checks whether the uploaded file is a CSV
•	Creates the Airflow payload
•	Authenticates using the Cloud Run service account
•	Triggers the Airflow DAG using the Airflow REST API
Payload sent to Airflow:
{
  "conf": {
    "bucket": "niko-health",
    "file_path": "employee/employee_1.csv"
  }
}
________________________________________
Step 5
Airflow DAG receives the runtime parameters.
The DAG contains two tasks:
1.	Read runtime configuration.
2.	Submit a Dataproc Serverless batch.
Arguments passed to Dataproc:
bucket
file_path
________________________________________
Step 6
Dataproc Serverless executes the PySpark program.
The Spark job performs the following transformations:
•	Read CSV from Cloud Storage.
•	Remove duplicate records.
•	Remove records with NULL Employee IDs.
•	Keep only records where Salary > 500.
•	Display transformed records.
•	Load processed data into BigQuery.
________________________________________
Step 7
Spark writes data into BigQuery using the Spark BigQuery Connector.
Destination Table
Project : gcp-free-trail-pavan-2026

Dataset : employee_niko_health

Table : employee_1
Temporary staging bucket
niko-health-temp
________________________________________
Airflow DAG
The Airflow DAG performs the following:
•	Reads runtime parameters from dag_run.conf
•	Prints the received configuration
•	Starts a Dataproc Serverless batch
•	Passes the bucket name and file path to the PySpark script
________________________________________
PySpark Transformations
The PySpark application performs:
•	Read CSV file
•	Infer schema
•	Remove duplicate records
•	Remove NULL employee IDs
•	Filter salary greater than 500
•	Load data into BigQuery
________________________________________
Cloud Run Function
Responsibilities:
•	Triggered by Eventarc
•	Reads Cloud Storage event
•	Validates CSV files
•	Generates OAuth access token
•	Calls the Airflow REST API
•	Starts the Airflow DAG
________________________________________
IAM Roles Used
Cloud Run Service Account
•	Authentication to call Airflow REST API
Composer Service Account
•	Dataproc Editor
•	Service Account User
Dataproc Service Account
•	Storage Object Viewer
•	Storage Object Admin
•	BigQuery Job User
•	BigQuery Data Editor
________________________________________
Challenges Faced
1. Cloud Run Function Error
Issue
TypeError: byte indices must be integers
Resolution
Added the CloudEvent decorator:
@functions_framework.cloud_event
________________________________________
2. Airflow Authentication Error
Issue
401 Unauthorized
Resolution
Configured OAuth authentication using the Cloud Run service account.
________________________________________
3. BigQuery Write Error
Issue
Either temporary or persistent GCS bucket must be set
Resolution
Created a temporary bucket:
niko-health-temp
Configured:
.option("temporaryGcsBucket", "niko-health-temp")
________________________________________
4. Dataproc Batch Failure
Issue
Insufficient CPUS_ALL_REGIONS quota
Resolution
Reviewed project quotas, checked running Dataproc batches, and planned to reduce requested resources or request additional quota.
________________________________________
Key Learnings
•	Event-driven architecture
•	Cloud Storage events
•	Eventarc triggers
•	Cloud Run Functions
•	CloudEvents
•	OAuth authentication
•	Airflow REST API
•	Apache Airflow DAGs
•	Dataproc Serverless
•	PySpark transformations
•	Spark BigQuery Connector
•	Temporary GCS staging bucket
•	BigQuery data loading
•	IAM roles and service accounts
•	Debugging and troubleshooting GCP services
________________________________________
End-to-End Flow
Upload CSV to Cloud Storage
          │
          ▼
Cloud Storage Event
          │
          ▼
Eventarc
          │
          ▼
Cloud Run Function
          │
          ▼
Trigger Airflow DAG
          │
          ▼
Dataproc Serverless
          │
          ▼
PySpark Transformations
          │
          ▼
Temporary GCS Bucket
          │
          ▼
BigQuery
This project demonstrates how to build an automated, scalable, serverless data ingestion pipeline using Google Cloud Platform services.

