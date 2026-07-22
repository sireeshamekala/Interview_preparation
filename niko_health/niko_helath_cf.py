import functions_framework
import requests
import google.auth
from google.auth.transport.requests import Request

AIRFLOW_URL = (
    "https://4569c1b9c89948f084b7db4eae330f00-dot-us-central1."
    "composer.googleusercontent.com/api/v1/dags/"
    "employee_dataproc_serverless/dagRuns"
)


@functions_framework.cloud_event
def trigger_airflow(cloud_event):

    data = cloud_event.data

    bucket = data["bucket"]
    file_name = data["name"]

    print(f"Bucket: {bucket}")
    print(f"File: {file_name}")

    # Process only CSV files
    if not file_name.lower().endswith(".csv"):
        print("Skipping non-CSV file.")
        return

    payload = {
        "conf": {
            "bucket": bucket,
            "file_path": file_name
        }
    }

    # Get OAuth Access Token
    credentials, project = google.auth.default()
    credentials.refresh(Request())

    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        AIRFLOW_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()