import os, json
from google.cloud import storage, bigquery

def load_json_to_bq(event, context):
    bucket_name = event['bucket']
    file_name = event['name']

    if not file_name.endswith('.json'):
        print("Not a JSON file, skipping.")
        return

    client = storage.Client()
    bq_client = bigquery.Client()

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    contents = blob.download_as_text()
    data = json.loads(contents)

    table_id = os.environ["BQ_TABLE_ID"]  # format: project.dataset.table

    errors = bq_client.insert_rows_json(table_id, data)
    if errors:
        print("Errors:", errors)
    else:
        print("✅ Data loaded into BigQuery")