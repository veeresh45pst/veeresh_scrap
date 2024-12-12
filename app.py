import streamlit as st
import pandas as pd
from job_Scraper import run_scraping
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Job Scraper", layout="wide")

st.title("Job Scraper App")

job_role = st.text_input("Enter Job Role")
location = st.text_input("Enter Location")

def start_scraping():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    st.write("Scraping in progress, please wait...")
    jobs, under_review_jobs = run_scraping(job_role, location)
    
    driver.quit()  

    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv("real_jobs.csv", index=False)
        st.write("Real Jobs")
        st.dataframe(df)

    if under_review_jobs:
        df_under_review = pd.DataFrame(under_review_jobs)
        df_under_review.to_csv("under_review_jobs.csv", index=False)
        st.write("Under Review Jobs")
        st.dataframe(df_under_review)

    if os.path.exists("real_jobs.csv"):
        with open("real_jobs.csv", "rb") as f:
            st.download_button(
                label="Download Real Job Data",
                data=f,
                file_name="real_jobs.csv",
                mime="text/csv"
            )
    else:
        st.write("No real job data available to download.")

    if os.path.exists("under_review_jobs.csv"):
        with open("under_review_jobs.csv", "rb") as f:
            st.download_button(
                label="Download Under Review Job Data",
                data=f,
                file_name="under_review_jobs.csv",
                mime="text/csv"
            )
    else:
        st.write("No under review job data available to download.")

if st.button("Start Scraping"):
    start_scraping()
    st.write("Scraping has started. Please wait for completion.")
