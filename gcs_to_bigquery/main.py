import os
from google.cloud import bigquery

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")

def main(request):
    request_json = request.get_json()
    bucket = request_json["bucket"]
    name = request_json["name"]

    uri = f"gs://{bucket}/{name}"
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition="WRITE_APPEND"
    )
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()
    print(f"✅ Loaded {uri} into {table_ref}")
    return "✅ BigQuery Load Triggered"
