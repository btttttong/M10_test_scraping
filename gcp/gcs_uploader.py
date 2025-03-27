from google.cloud import storage
from gcp.config import BUCKET_NAME, GCS_PATH, CSV_FILENAME

def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(GCS_PATH)
    blob.upload_from_filename(CSV_FILENAME)
    print(f"✅ Uploaded to GCS: gs://{BUCKET_NAME}/{GCS_PATH}")