import time
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


class ParseCSV(beam.DoFn):

    def process(self, line):

        cols = line.split(",")

        yield {
            "sale_id": int(cols[0]),
            "customer_id": cols[1],
            "product": cols[2],
            "price": float(cols[3]),
            "city": cols[4]
        }


class RemoveInvalidRecords(beam.DoFn):

    def process(self, record):

        # customer_id should not be null
        if record["customer_id"] == "":
            return

        # price should be greater than 0
        if record["price"] <= 0:
            return

        record["customer_id"] = int(record["customer_id"])

        yield record


pipeline_options = PipelineOptions(
    runner="DataflowRunner",
    project="gcp-free-trail-pavan-2026",
    region="us-central1",
    temp_location="gs://dataplex-retail-demo/temp",
    staging_location="gs://dataplex-retail-demo/staging",
    service_account_email="dataflow-runner@gcp-free-trail-pavan-2026.iam.gserviceaccount.com",
    job_name=f"sales-clean-{int(time.time())}",
    save_main_session=True
)

with beam.Pipeline(options=pipeline_options) as p:

    (
        p

        | "Read CSV"
        >> beam.io.ReadFromText(
            "gs://dataplex-retail-demo/raw/sales.csv",
            skip_header_lines=1
        )

        | "Parse CSV"
        >> beam.ParDo(ParseCSV())

        # Remove duplicate sale_id
        | "PairWithSaleId"
        >> beam.Map(lambda row: (row["sale_id"], row))

        | "GroupBySaleId"
        >> beam.GroupByKey()

        | "KeepFirstRecord"
        >> beam.Map(lambda kv: next(iter(kv[1])))

        | "Remove Invalid Records"
        >> beam.ParDo(RemoveInvalidRecords())

        | "Write To BigQuery"
        >> beam.io.WriteToBigQuery(
            table="gcp-free-trail-pavan-2026:retail_demo.sales_clean",

            schema="""
                sale_id:INTEGER,
                customer_id:INTEGER,
                product:STRING,
                price:FLOAT,
                city:STRING
            """,

            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,

            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
    )