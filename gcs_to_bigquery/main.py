import os, json
from google.cloud import bigquery, storage

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")

def main(request):
    request_json = request.get_json()
    bucket_name = request_json["bucket"]
    file_name = request_json["name"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    records = json.loads(content)

    client = bigquery.Client()
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    errors = client.insert_rows_json(table_ref, records)
    if errors:
        print(f"❌ Errors occurred: {errors}")
    else:
        print(f"✅ Loaded {len(records)} records to {table_ref}")
    return "✅ JSON loaded to BigQuery"
