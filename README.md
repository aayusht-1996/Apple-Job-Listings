# Apple Careers Job Scraper

This project is a web scraper built using Python and Selenium to extract **all active job postings** from the [Apple Careers site](https://jobs.apple.com/en-us/search). It navigates through every available page and captures detailed information about each job listing.

## 🔍 What It Captures

- Job Title
- Team / Department
- Location (with fallback for alternate formats)
- Post Date
- Job ID
- Job URL

## 🚀 Features

- Fully automated scrolling through all available job pages
- Handles dynamic elements and varied HTML structures
- Supports both visible and fallback location formats
- Outputs structured data to a CSV file

## 📂 Output

The scraped data is saved as `apple_all_jobs.csv` with the following columns:

| Job ID | Title | Team | Location | Post Date | URL |
|--------|-------|------|----------|-----------|-----|


