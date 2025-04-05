from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup
options = Options()
# options.add_argument("--headless=new")  # Enable for background scraping
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
job_data = []

def get_job_info_on_page():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.link-inline.t-intro.word-wrap-break-word'))
        )
    except TimeoutException:
        print("⚠️ Timed out waiting for job listings.")
        return

    job_links = driver.find_elements(By.CSS_SELECTOR, 'a.link-inline.t-intro.word-wrap-break-word')
    print(f"📄 Found {len(job_links)} job titles on this page.")

    for link in job_links:
        try:
            title = link.text.strip()
            url = link.get_attribute("href")
            job_id = url.split("/")[-2] if url else "N/A"
            container = link.find_element(By.XPATH, "../../..")

            try:
                team = container.find_element(By.CSS_SELECTOR, "span.team-name").text.strip()
            except:
                team = "N/A"

            try:
                location = container.find_element(By.CSS_SELECTOR, "span.table--advanced-search__location-sub").text.strip()
            except:
                try:
                    location = container.find_element(By.CSS_SELECTOR, "span[id^='search-store-name-container']").text.strip()
                except:
                    location = "N/A"

            try:
                post_date = container.find_element(By.CSS_SELECTOR, "span.job-posted-date").text.strip()
            except:
                post_date = "N/A"

            job_data.append({
                "Job ID": job_id,
                "Title": title,
                "Team": team,
                "Location": location,
                "Post Date": post_date,
                "URL": url
            })

        except Exception as e:
            print(f"⚠️ Skipping job due to: {e}")
            continue

def go_to_next_page():
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'button.icon.icon-chevronend')
        if next_button.is_enabled():
            next_button.click()
            print("➡️ Moving to next page...")
            time.sleep(3)
            return True
    except NoSuchElementException:
        print("🚫 No next page button found.")
    return False

def scrape_all_pages():
    print("🌐 Opening Apple Careers...")
    driver.get("https://jobs.apple.com/en-us/search")
    time.sleep(5)

    page = 1
    while True:
        print(f"\n📄 Scraping page {page}...")
        get_job_info_on_page()
        if not go_to_next_page():
            break
        page += 1

    driver.quit()

    if job_data:
        df = pd.DataFrame(job_data)
        df.to_csv("apple_all_jobs.csv", index=False)
        print(f"\n✅ Done. Scraped {len(df)} jobs and saved to 'apple_all_jobs.csv'")
    else:
        print("⚠️ No job data scraped.")

if __name__ == "__main__":
    scrape_all_pages()
