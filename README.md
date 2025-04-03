# 🔥 GCP Data Pipeline: GCS to BigQuery

This project deploys two Cloud Run services using Cloud Build:
1. **extract-to-gcs** — Extracts data and uploads it to GCS.
2. **gcs-to-bigquery** — Loads data from GCS into BigQuery.

---

## ✅ Prerequisites

Before you begin, make sure you have:

- A Google Cloud project with billing enabled
- A GCS bucket already created
- A BigQuery dataset and table ready (or plan to create them)
- Enabled these APIs:
  - Cloud Run
  - Cloud Build
  - Artifact Registry
  - BigQuery
  - Cloud Storage
- (Optional) Git and Cloud SDK installed **OR** use [Google Cloud Shell](https://shell.cloud.google.com)

---

## 📥 Clone This Repo

```bash
git clone https://github.com/btttttong/M10_test_scraping.git
cd to repo
```

---

## 📁 Project Structure

```
.
├── extract_to_gcs/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── gcs_to_bigquery/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── cloudbuild.yaml
└── README.md
```

---

## 🚀 Deploy with Cloud Build

Run this command:

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_BUCKET_NAME=your-bucket-name
```

---

## 🛠️ Environment Variables

These are passed into the services:

| Variable      | Description                         |
|---------------|-------------------------------------|
| `PROJECT_ID`  | GCP project ID                      |
| `BUCKET_NAME` | Name of your GCS bucket             |
| `DATASET_ID`  | BigQuery dataset name               |
| `TABLE_ID`    | BigQuery table name                 |

---

## 🌐 Accessing the Services

- `extract-to-gcs` is public (unauthenticated)
- `gcs-to-bigquery` is private (authenticated or internal trigger only)

---

## 📦 Deployment Output

- Two services deployed to **Cloud Run**
- Two container images stored in **Artifact Registry**
- Logs available in **Cloud Logging**

---

## 🧽 Cleanup

To delete services:

```bash
gcloud run services delete extract-to-gcs --region=us-central1
gcloud run services delete gcs-to-bigquery --region=us-central1
```

---

Made with ☕ + 💻 by BT 💖
