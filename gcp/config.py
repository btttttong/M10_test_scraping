import os

PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")
CSV_FILENAME = "output/amazon_scraped_data.csv"
GCS_PATH = f"scraped_data/{TABLE_ID}.csv"