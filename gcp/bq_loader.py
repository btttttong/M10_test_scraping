from google.cloud import bigquery
from gcp.config import PROJECT_ID, DATASET_ID, TABLE_ID, BUCKET_NAME, GCS_PATH

def load_to_bigquery():
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{TABLE_ID}"
    uri = f"gs://{BUCKET_NAME}/{GCS_PATH}"

    print("client", client)
    print("table_ref", table_ref)
    print("uri", uri)

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE"
    )

    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()
    print(f"✅ Loaded to BigQuery: {table_ref}")