from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def classify_job(job):
    fake_keywords = ['Cash Payment']
    if job['Job Description'] == 'N/A':
        return 'Fake'
    for keyword in fake_keywords:
        if keyword.lower() in job['Job Description'].lower():
            return 'Fake'
    return 'Real'

def run_scraping(job_role, location):
    driver = webdriver.Chrome()
    BASE_URL = f"https://in.indeed.com/jobs?q={job_role}&l={location}"

    driver.get(BASE_URL)
    time.sleep(3)

    jobs = []
    under_review_jobs = []

    while True:
        for _ in range(5):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_elements = soup.find_all("div", class_="job_seen_beacon")

        for job_element in job_elements:
            title_element = job_element.find("h2", class_="jobTitle")
            job_title = title_element.text.strip() if title_element else "N/A"

            company_element = job_element.find("span", {"data-testid": "company-name"})
            company_name = company_element.text.strip() if company_element else "N/A"

            job_id_element = job_element.find("a", {"data-jk": True})
            job_id = job_id_element["data-jk"] if job_id_element else "N/A"

            location_element = job_element.find("div", {"class": lambda x: x and "location" in x.lower()})
            job_location = location_element.text.strip() if location_element else "N/A"

            job_link = f"https://in.indeed.com/viewjob?jk={job_id}" if job_id != "N/A" else None
            job_description = "N/A"
            if job_link:
                driver.get(job_link)
                time.sleep(3)
                job_soup = BeautifulSoup(driver.page_source, "html.parser")
                description_element = job_soup.find("div", id="jobDescriptionText")
                job_description = description_element.text.strip() if description_element else "N/A"

            
            
            
            posted_date_element = job_element.find("span", class_="date")
            posted_date = posted_date_element.text.strip() if posted_date_element else "N/A"

            job_data = {
                "Job ID": job_id,
                "Job Title": job_title,
                "Company Name": company_name,
                "Job Location": job_location,
                "Job Description": job_description
            }

            classification = classify_job(job_data)
            job_data["Classification"] = classification

            if classification == "Fake":
                under_review_jobs.append(job_data)
            else:
                jobs.append(job_data)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Next"]')
            next_button.click()
            time.sleep(3)
        except Exception:
            print("No more pages to scrape.")
            break

    driver.quit()

    # Save to CSV
    save_to_csv(jobs, 'real_jobs.csv')
    save_to_csv(under_review_jobs, 'under_review_jobs.csv')

    return jobs, under_review_jobs

def save_to_csv(jobs, filename):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)