import os
import json
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# This file was used to populate the raw folder

def fetch_tickers_and_companies(market, url, suffix, log_callback=None):
    
    def log(message, level="INFO"):
        print(message)
        if log_callback and "⚠️" not in message:
            log_callback(message)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    all_data = []
    ticker_idx = None
    company_idx = None

    def handle_popups():
        try:
            cookie_buttons = driver.find_elements(By.XPATH,
                "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or " +
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree') or " +
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'got it') or " +
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'consent')]"
            )
            for btn in cookie_buttons:
                if btn.is_displayed():
                    log("  🍪 Clicking cookie consent.")
                    btn.click()
                    time.sleep(1)
                    break
        except Exception as e:
            log(f"  ⚠️ Cookie popup not handled: {e}")

        try:
            close_buttons = driver.find_elements(By.XPATH,
                "//button[contains(., '×') or @aria-label='Close'] | " +
                "//div[contains(@class, 'close') or contains(@class, 'dismiss')] | " +
                "//button[contains(@class, 'close')]"
            )
            for btn in close_buttons:
                if btn.is_displayed():
                    log("  ❌ Closing modal or sign-up popup.")
                    btn.click()
                    time.sleep(1)
                    break
        except Exception as e:
            log(f"  ⚠️ Modal popup not handled: {e}")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        handle_popups() 

        table = driver.find_element(By.TAG_NAME, "table")
        thead = table.find_element(By.TAG_NAME, "thead")
        headers = [th.text.strip().lower() for th in thead.find_elements(By.TAG_NAME, "th")]

        log(f"  Table columns: {headers}")

        for i, h in enumerate(headers):
            if h in ["symbol", "ticker"]:
                ticker_idx = i
            if h in ["company name", "name", "company"]:
                company_idx = i

        if ticker_idx is None or company_idx is None:
            log("  ❌ Required columns not found. Skipping market.")
            return []

        page_count = 0
        max_pages = 1000
        while page_count < max_pages:
            page_count += 1
            log(f"  Processing page {page_count} ...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )
            handle_popups()  

            rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) > max(ticker_idx, company_idx):
                    ticker = cols[ticker_idx].text.strip()
                    company = cols[company_idx].text.strip()
                    if ticker:
                        all_data.append([ticker + suffix, company])

            
            try:
                next_button = driver.find_element(By.XPATH, "//button[contains(., 'Next') or contains(., '›')] | //a[contains(., 'Next') or contains(., '›')]")
                if not next_button.is_enabled() or 'disabled' in next_button.get_attribute("class").lower():
                    log("  ✅ Reached last page.")
                    break
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(1.5)
            except Exception as e:
                log(f"  ⚠️ No more pages or next button issue: {e}")
                break
    finally:
        driver.quit()

    return all_data

def save_tickers_and_companies(all_data, market):
    os.makedirs("data/raw", exist_ok=True)
    out_path = f"data/raw/{market}.csv"
    with open(out_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Company"])
        writer.writerows(all_data)
    print(f"✅ Saved {len(all_data)} rows to {out_path}")

def main():
    with open("data/configs/markets.json", "r", encoding="utf-8") as f:
        markets = json.load(f)

    for market, (url, suffix) in markets.items():
        if market not in ["NASDAQ", "NYSE"]:
            break
        print(f"\n🔎 Scraping {market} from {url} ...")
        try:
            all_data = fetch_tickers_and_companies(market, url, suffix)
            if all_data:
                save_tickers_and_companies(all_data, market)
            else:
                print(f"❌ No data found for {market}")
        except Exception as e:
            print(f"❌ Failed to scrape {market}: {e}")


if __name__ == "__main__":
    main()
