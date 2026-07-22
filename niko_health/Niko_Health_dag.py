from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator

PROJECT_ID = "gcp-free-trail-pavan-2026"
REGION = "us-central1"

SPARK_FILE = "gs://niko-health/spark-code/Niko_Health_dataproc.py"

default_args = {
    "owner": "airflow",
    "retries": 1
}

with DAG(
    dag_id="employee_dataproc_serverless",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dataproc", "bigquery"],
) as dag:

    def print_conf(**context):

        conf = context["dag_run"].conf

        print(conf)

    read_conf = PythonOperator(
        task_id="read_configuration",
        python_callable=print_conf
    )

    dataproc_batch = DataprocCreateBatchOperator(
        task_id="run_dataproc_batch",
        project_id=PROJECT_ID,
        region=REGION,
        batch={
            "pyspark_batch": {
                "main_python_file_uri": SPARK_FILE,
                "args": [
                    "{{ dag_run.conf['bucket'] }}",
                    "{{ dag_run.conf['file_path'] }}"
                ],
            },
            "environment_config": {
                "execution_config": {
                    "service_account": "niko-helath@gcp-free-trail-pavan-2026.iam.gserviceaccount.com"
                }
            }
        },
    )

    read_conf >> dataproc_batch