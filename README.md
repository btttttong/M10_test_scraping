# 🛠️ GCP ETL Pipeline (Cloud Run + Scheduler + BigQuery)

This project demonstrates a complete **ETL pipeline on GCP** using two separate Cloud Run services:

---

## ✅ Pipeline Overview

1. **Cloud Run #1: `extract_to_gcs`**
   - Scrapes data from Amazon (e.g. IELTS books)
   - Saves the result as a CSV
   - Uploads the CSV to **Google Cloud Storage (GCS)**

2. **Cloud Run #2: `gcs_to_bigquery`**
   - Triggered automatically when a file is uploaded to GCS
   - Loads the uploaded CSV into a **BigQuery table**

3. **Cloud Scheduler**
   - Triggers the first Cloud Run service (`extract_to_gcs`) on a set schedule

---

## 📁 Folder Structure

```
etl-pipeline/
├── extract_to_gcs/         # Function 1: Scrape and upload to GCS
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── gcs_to_bigquery/        # Function 2: Triggered by GCS upload, loads to BQ
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── .gitignore
└── .env.example            # Template for environment variables
```

---

## ⚙️ Environment Variables (`.env`)

```
PROJECT_ID=your-gcp-project-id
BUCKET_NAME=your-bucket-name
DATASET_ID=your_bigquery_dataset
TABLE_ID=your_table_name
```

---

## 🚀 Deployment Guide

### 1. Build & Deploy Cloud Run Service 1

```bash
cd extract_to_gcs
gcloud builds submit --tag gcr.io/$PROJECT_ID/extract-to-gcs
gcloud run deploy extract-to-gcs \
  --image gcr.io/$PROJECT_ID/extract-to-gcs \
  --region us-central1 \
  --set-env-vars PROJECT_ID=$PROJECT_ID,BUCKET_NAME=$BUCKET_NAME \
  --service-account your-service-account@your-project.iam.gserviceaccount.com
```

---

### 2. Deploy Cloud Run Service 2 (BQ Loader)

```bash
cd ../gcs_to_bigquery
gcloud builds submit --tag gcr.io/$PROJECT_ID/gcs-to-bigquery
gcloud run deploy gcs-to-bigquery \
  --image gcr.io/$PROJECT_ID/gcs-to-bigquery \
  --region us-central1 \
  --set-env-vars PROJECT_ID=$PROJECT_ID,DATASET_ID=$DATASET_ID,TABLE_ID=$TABLE_ID \
  --service-account your-service-account@your-project.iam.gserviceaccount.com
```

---

### 3. Connect GCS to Cloud Run Trigger (BQ Loader)

1. Enable GCS notifications via Pub/Sub.
2. Create a Pub/Sub topic.
3. Subscribe to the topic with a **push endpoint** → your `gcs-to-bigquery` Cloud Run URL.

---

### 4. Set up Cloud Scheduler to Trigger Scraping

```bash
gcloud scheduler jobs create http scrape-job \
  --schedule="0 8 * * *" \
  --uri="https://REGION-run-url" \
  --http-method=GET \
  --oidc-service-account-email=your-service-account@your-project.iam.gserviceaccount.com
```

---

## ✅ Result

- Amazon data scraped daily (or on your schedule)
- CSV saved in GCS
- Automatically loaded into BigQuery 🎯

---

## 🙌 Credits

Built with ❤️ using:
- Python
- Selenium + BeautifulSoup
- Google Cloud Run, GCS, BigQuery, Pub/Sub, Scheduler
