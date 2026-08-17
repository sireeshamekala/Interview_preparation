EXPORT DATA ... SELECT ... WHERE ... → Exports the selected BigQuery table data as Snappy-compressed Parquet files to GCS, applying the specified partition filter.
client.extract_table(...) → Directly exports the entire BigQuery table to the specified GCS location in the format defined by job_config.
load_table_from_uri(...) → Loads the file(s) from GCS into the specified BigQuery table, using the format/schema/write settings in job_config


if partition_field == '_PARTITIONTIME':
                    partition_filter = "_PARTITIONTIME IS NOT NULL"
                else:
                    partition_filter = f"`{partition_field}` IS NOT NULL"
                export_query = (
                    f"EXPORT DATA OPTIONS("
                    f" uri='{destination_uri}',"
                    f" format='PARQUET',"
                    f" compression='SNAPPY',"
                    f" overwrite=true) AS "
                    f"SELECT * FROM `{table_ref}` "
                    f"WHERE {partition_filter}"
                )

extract_job = client.extract_table(table_ref, destination_uri, job_config=job_config)



Recovery
recover_job = get_bq_client(p, gcs_dataset_service_account).load_table_from_uri(
                destination=f"{p}.{d}.{t}",
                source_uris=source_uri,
                job_config=job_config
            )
