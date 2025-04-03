from flask import Flask
import os
from google.cloud import bigquery, storage

app = Flask(__name__)

@app.route('/')
def run_job():
    bucket_name = os.environ.get("BUCKET_NAME")
    project_id = os.environ.get("PROJECT_ID")
    dataset_id = os.environ.get("DATASET_ID")
    table_id = os.environ.get("TABLE_ID")

    # Your logic here (simplified)
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print(f"Found file: {blob.name}")

    return "BigQuery load job triggered successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)