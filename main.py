from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
import time 
import random



def check_kindle_unlimited(search_url):
    # 1. Send the GET request
    HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/87.0.4280.67 Safari/537.36"
    )
}

    response = requests.get(search_url, headers=HEADERS)
    print(response.text[:2000])
    
    if response.status_code != 200:
        return "I am a robot"  # or handle errors differently

    # 2. Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 3. Look for an <img> with alt="Kindle Unlimited" (or partial match)
    #    This is an example approach; actual alt text might differ.
    images = soup.find_all("img", alt="Kindle Unlimited")
    if images:
        return "Available"

    return "Not Available"

def main():
    file_path = "storygraph2025-01.csv"
    tbr_list = pd.read_csv(file_path)

    ku_availability = []

    for index, row in tbr_list.iterrows():
        title = row["Title"]
        authors = row["Authors"]

        encoded_title = quote_plus(title)
        encoded_authors = quote_plus(authors)
        search_url = f"https://www.amazon.com/s?k={encoded_title}+{encoded_authors}"

        # Check KU availability
        availability = check_kindle_unlimited(search_url)
        ku_availability.append(availability)

        print(f"Row {index}: {title}")
        print(f"  => URL: {search_url}")
        print(f"  => Availability: {availability}")
        print("---")

        time.sleep(random.uniform(3, 6))  # Sleep between 3-6 seconds

    

if __name__ == "__main__":
    main()