Cloud Run Function 
Objective
The Cloud Run Function acts as the entry point of the event-driven pipeline. It receives file upload events from Cloud Storage through Eventarc and triggers downstream processing (Airflow/Dataflow/Dataproc).
________________________________________
Architecture
Cloud Storage
      │
Object Finalized Event
      │
      ▼
Eventarc
      │
      ▼
Cloud Run Function
      │
      ▼
Airflow / Dataflow / Dataproc
________________________________________
Concepts Learned
1. Cloud Run Functions
•	Serverless compute service.
•	Runs only when an event occurs.
•	No infrastructure or server management.
•	Automatically scales based on incoming requests.
•	Supports HTTP and Event-driven triggers.
________________________________________
2. Event-Driven Architecture
Instead of manually running the pipeline, it starts automatically when a new file is uploaded.
Flow:
Upload File

↓

Cloud Storage Event

↓

Eventarc

↓

Cloud Run Function

↓

Trigger Processing
________________________________________
3. Eventarc
Learned how Eventarc routes Cloud Storage events to Cloud Run.
Event Used:
google.cloud.storage.object.v1.finalized
This event occurs whenever a new object is successfully created in Cloud Storage.
________________________________________
4. Functions Framework
Used:
import functions_framework
Decorator:
@functions_framework.cloud_event
Purpose:
•	Receives CloudEvents from Eventarc.
•	Converts the incoming event into a Python object.
________________________________________
5. CloudEvent
Learned how to read Cloud Storage event information.
Example event:
{
  "bucket":"niko-health",
  "name":"employee/employee_1.csv"
}
Read values:
bucket = data["bucket"]
file_name = data["name"]
________________________________________
6. File Validation
Only CSV files are processed.
if not file_name.lower().endswith(".csv"):
    return
This prevents triggering downstream services for unsupported file types.
________________________________________
7. Runtime Payload
Created a payload containing runtime parameters.
payload = {
    "conf": {
        "bucket": bucket,
        "file_path": file_name
    }
}
These parameters are passed to the downstream service.
________________________________________
8. Authentication
Learned how Cloud Run authenticates using its attached Service Account.
Used:
credentials, project = google.auth.default()
Refresh access token:
credentials.refresh(Request())
This generates an OAuth access token used for secure API calls.
________________________________________
9. REST API Calls
Used Python Requests library.
import requests
POST request:
requests.post(...)
Used to trigger:
•	Airflow REST API
•	Dataflow REST API
•	Dataproc Batch API
________________________________________
10. HTTP Headers
Added authentication token.
headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}
________________________________________
11. Logging
Used:
print()
to log:
•	Bucket name
•	File name
•	Response status
•	API response
Logs are available in Cloud Logging.
________________________________________
12. Error Handling
Used:
response.raise_for_status()
Raises an exception when the API call fails.
Examples:
•	401 Unauthorized
•	404 Not Found
•	500 Internal Server Error
________________________________________
Downstream Services That Can Be Triggered
Option 1 - Cloud Run → Airflow
Cloud Storage

↓

Eventarc

↓

Cloud Run Function

↓

Airflow DAG

↓

Dataproc/Dataflow

↓

BigQuery
Purpose:
Used for workflow orchestration, retries, scheduling, and multiple tasks.
________________________________________
Option 2 - Cloud Run → Dataflow
Cloud Storage

↓

Eventarc

↓

Cloud Run Function

↓

Dataflow Job

↓

BigQuery
Purpose:
Used for Apache Beam batch or streaming pipelines.
________________________________________
Option 3 - Cloud Run → Dataproc Serverless
Cloud Storage

↓

Eventarc

↓

Cloud Run Function

↓

Dataproc Serverless

↓

BigQuery
Purpose:
Used to execute Spark/PySpark jobs directly without Airflow.
________________________________________
IAM Concepts Learned
Cloud Run Function uses a Service Account to:
•	Read Cloud Storage event information.
•	Generate OAuth access tokens.
•	Call Google Cloud APIs.
•	Trigger Airflow.
•	Launch Dataflow jobs.
•	Submit Dataproc batches.
________________________________________
Python Libraries Used
functions_framework
Handles CloudEvents.
requests
Used for REST API calls.
google.auth
Retrieves default credentials.
Request
Refreshes OAuth access tokens.
________________________________________
End-to-End Flow
1. User uploads employee_1.csv

↓

2. Cloud Storage generates Object Finalized event

↓

3. Eventarc receives the event

↓

4. Cloud Run Function starts

↓

5. Reads bucket name

↓

6. Reads uploaded file name

↓

7. Validates CSV file

↓

8. Creates runtime payload

↓

9. Generates OAuth access token

↓

10. Calls REST API

↓

11. Triggers Airflow / Dataflow / Dataproc

↓

12. Downstream service starts data processing
