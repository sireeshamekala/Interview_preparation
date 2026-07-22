import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ----------------------------------------------------
# Read Arguments from Airflow
# ----------------------------------------------------

bucket = sys.argv[1]
file_path = sys.argv[2]

input_file = f"gs://{bucket}/{file_path}"

print(f"Reading File : {input_file}")

# ----------------------------------------------------
# Spark Session
# ----------------------------------------------------

spark = (
    SparkSession.builder
    .appName("Employee Processing")
    .getOrCreate()
)

# ----------------------------------------------------
# Read CSV
# ----------------------------------------------------

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_file)
)

print("Input Records :", df.count())

# ----------------------------------------------------
# Remove Duplicate Records
# ----------------------------------------------------

df = df.dropDuplicates()

# ----------------------------------------------------
# Remove Null Employee IDs
# ----------------------------------------------------

df = df.filter(col("emp_id").isNotNull())

# ----------------------------------------------------
# Salary should be greater than 500
# ----------------------------------------------------

df = df.filter(col("salary") > 500)

# ----------------------------------------------------
# Display Result
# ----------------------------------------------------

print("Records After Transformation :", df.count())

df.show(truncate=False)

# ----------------------------------------------------
# Write to BigQuery
# ----------------------------------------------------

(
    df.write
    .format("bigquery")
    .option(
        "table",
        "gcp-free-trail-pavan-2026.employee_niko_health.employee_1"
    )
    .option(
        "temporaryGcsBucket",
        "niko-health-temp"
    )
    .mode("append")
    .save()
)

print("Data Loaded Successfully into BigQuery")

spark.stop()