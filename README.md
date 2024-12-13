Job Scraping and Classification Streamlit Application

This project is a Streamlit application that scrapes job listings from various job boards, classifies them using the Groq API, and provides options to download the results. It identifies and separates potentially fake job listings for manual review. Features

Streamlit Application

User-friendly interface with input fields for Job Role and Location.
Start button to initiate the job scraping process.
Progress status display.
Options to download results directly from the app.
Job Scraping

Scrapes job listings from four job boards: Indeed, Glassdoor, LinkedIn, and Monster.
Uses BeautifulSoup for static pages and Selenium for dynamic pages.
Implements pagination to scrape all relevant data.
API Integration

Uses the Groq API to classify job descriptions and determine their legitimacy.
Categorizes jobs into specific categories (e.g., IT, Marketing, Healthcare).
Handling Fake Jobs

Jobs flagged as "Fake" are stored in a separate CSV file named Under_Review.csv for manual review.
Output Results

Stores processed jobs in a master CSV file with the following columns:
Title
Company
Location
Description
Classification
Provides download links for both the master file and the under-review file in the Streamlit app.
Installation

Clone the repository: bash git clone https://github.com/vanishree956/job-scraping-app.git cd job-scraping-app

Install the required dependencies: bash pip install -r requirements.txt

Set up environment variables for the Groq API key and any other necessary configuration.

Usage

Run the Streamlit application: bash pyhton -m streamlit run app.py

Open the application in your web browser. You should see input fields for Job Role and Location.

Enter the desired Job Role and Location and click the "Start" button to begin scraping.

The application will display the progress status and notify you when the scraping is complete.

Download the results using the provided download links for the master file and the under-review file.

File Structure

app.py: Main Streamlit application script.
job_Scraper.py: Script containing functions for scraping job boards.
setAPI.py: Script for interacting with the Groq API.
requirements.txt: List of required Python packages.
README.md: This README file.
