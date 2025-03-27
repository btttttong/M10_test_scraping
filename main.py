# ✅ main.py
import csv, time, os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from gcp.gcs_uploader import upload_to_gcs
from gcp.bq_loader import load_to_bigquery
from gcp.config import CSV_FILENAME

load_dotenv()

# Setup Firefox driver
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
service = Service("./geckodriver")
driver = webdriver.Firefox(service=service, options=options)

# Create CSV
with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["Title", "Price", "Rating", "Link"])

def scrape_save_store():
    driver.get("https://www.amazon.com/s?k=IELTS+books")
    for page in range(1, 10):
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.select("div.s-main-slot div[data-component-type='s-search-result']")
        rows = []
        for p in products:
            title = p.select_one("h2.a-size-medium") or p.select_one("h2.a-size-base-plus")
            link = p.select_one("h2 a, a.a-link-normal.s-no-outline, a.s-link-style, a.a-button-text")
            price = p.select_one("span.a-price span.a-offscreen")
            rating = p.select_one("span.a-icon-alt")
            rows.append([
                title.text.strip() if title else "No title",
                price.text.strip() if price else "No price",
                rating.text.strip() if rating else "No rating",
                "https://www.amazon.com" + link["href"] if link and "href" in link.attrs else "No link",
            ])
        with open(CSV_FILENAME, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)
        try:
            next_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.s-pagination-next")))
            next_btn.click()
            time.sleep(3)
        except:
            break

    driver.quit()
    print("Scraping done.")

if __name__ == "__main__":
    scrape_save_store()
    upload_to_gcs()
    load_to_bigquery()
    print("✅ ETL pipeline complete!")
