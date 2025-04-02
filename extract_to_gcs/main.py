import os, time, json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from google.cloud import storage
from datetime import datetime
from datetime import datetime, timezone

PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
JSON_FILENAME = "/tmp/amazon_data.json"
GCS_PATH = f"scraped_data/amazon_data_{datetime.now(timezone.utc).isoformat()}.json"

def scrape_to_json():
    service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=service)
    driver.get("https://www.amazon.com/s?k=IELTS+books")

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.select("div[data-component-type='s-search-result']")

    data = []
    for p in products:
        title = (p.select_one("h2.a-size-medium") or p.select_one("h2.a-size-base-plus"))
        price = p.select_one("span.a-price span.a-offscreen")
        rating = p.select_one("span.a-icon-alt")
        link = p.select_one("h2 a")
        data.append({
            "title": title.text.strip() if title else "No title",
            "price": price.text.strip() if price else "No price",
            "rating": rating.text.strip() if rating else "No rating",
            "link": "https://www.amazon.com" + link["href"] if link else "No link"
        })

    with open(JSON_FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    driver.quit()

def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(GCS_PATH)
    blob.upload_from_filename(JSON_FILENAME)
    print(f"✅ Uploaded to GCS: gs://{BUCKET_NAME}/{GCS_PATH}")

def main(request=None):
    scrape_to_json()
    upload_to_gcs()
    return "✅ Scraped and uploaded JSON to GCS"
