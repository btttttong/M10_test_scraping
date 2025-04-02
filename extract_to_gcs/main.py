import csv, os, time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from google.cloud import storage

PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
CSV_FILENAME = "/tmp/amazon_scraped_data.csv"
GCS_PATH = f"scraped_data/amazon_scraped_data.csv"

def scrape_to_csv():
    service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=service)
    driver.get("https://www.amazon.com/s?k=IELTS+books")

    with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Rating", "Link"])
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.select("div[data-component-type='s-search-result']")
        for p in products:
            title = (p.select_one("h2.a-size-medium") or p.select_one("h2.a-size-base-plus"))
            price = p.select_one("span.a-price span.a-offscreen")
            rating = p.select_one("span.a-icon-alt")
            link = p.select_one("h2 a")
            writer.writerow([
                title.text.strip() if title else "No title",
                price.text.strip() if price else "No price",
                rating.text.strip() if rating else "No rating",
                "https://www.amazon.com" + link["href"] if link else "No link"
            ])
    driver.quit()

def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(GCS_PATH)
    blob.upload_from_filename(CSV_FILENAME)
    print(f"✅ Uploaded to GCS: gs://{BUCKET_NAME}/{GCS_PATH}")

def main(request=None):
    scrape_to_csv()
    upload_to_gcs()
    return "✅ Extracted and uploaded to GCS"
