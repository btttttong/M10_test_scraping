# 🚀 GCP Setup Guide for GCS to BigQuery Pipeline

This guide walks you through setting up the necessary GCP resources before deploying the project.

---

## ✅ 1. Create a GCP Project

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Click “Select Project” → “New Project”
- Name your project and remember the `PROJECT_ID`

---

## ✅ 2. Enable Required APIs

You can run this in **Cloud Shell**:

```bash
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    bigquery.googleapis.com \
    storage.googleapis.com
```

---

## ✅ 3. Create a GCS Bucket

```bash
gsutil mb -l us-central1 gs://your-bucket-name/
```

---

## ✅ 4. Create a BigQuery Dataset and Table

- Go to [BigQuery Console](https://console.cloud.google.com/bigquery)
- Create a dataset: `university`
- Create a table: `amazon_scraped_data`

You can import schema manually or define it in code later.

---

## ✅ 5. Clone This Repo

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Replace the repo link with your actual one if you're sharing it.

---

## ✅ 6. Deploy with Cloud Build

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_BUCKET_NAME=your-bucket-name
```

This will:
- Build Docker images
- Deploy services to Cloud Run
- Use the specified bucket and project settings

---

## ✅ 7. Test the Service

- Open the **Cloud Run URL** for `extract-to-gcs`
- You should see a success message and new files in GCS

---

## ✅ 8. Cleanup (Optional)

To avoid charges:

```bash
gcloud run services delete extract-to-gcs --region=us-central1
gcloud run services delete gcs-to-bigquery --region=us-central1
```

---

Made with ☕ + 💻 by BT 💖
