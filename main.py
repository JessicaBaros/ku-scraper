import pandas as pd
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import random

def check_kindle_unlimited(driver, search_url):
    try:
        # Navigate to the search URL
        driver.get(search_url)
        
        # Optional: Wait for the page to load completely
        time.sleep(random.uniform(2, 4))  # Adjust as needed

        # Look for an <img> with alt="Kindle Unlimited"
        # Using XPath to find the image
        # Adjust the XPath if necessary based on Amazon's HTML structure
        images = driver.find_elements(By.XPATH, "//img[@alt='Kindle Unlimited']")

        if images:
            return "Available"
        else:
            return "Not Available"
    
    except Exception as e:
        print(f"Error checking URL {search_url}: {e}")
        return "I am a muppet"

def main():
    # Initialize Selenium WebDriver with WebDriver Manager
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # Optional: Set window size
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Load your CSV file
    file_path = "storygraph2025-01.csv"
    tbr_list = pd.read_csv(file_path)
    
    ku_availability = []
    
    for index, row in tbr_list.iterrows():
        title = row["Title"]
        authors = row["Authors"]
    
        encoded_title = quote_plus(title)
        encoded_authors = quote_plus(authors)
        search_url = f"https://www.amazon.com/s?k={encoded_title}+{encoded_authors}"
    
        # Check KU availability using Selenium
        availability = check_kindle_unlimited(driver, search_url)
        ku_availability.append(availability)
    
        print(f"Row {index}: {title}")
        print(f"  => URL: {search_url}")
        print(f"  => Availability: {availability}")
        print("---")
    
        # Optional: Delay to mimic human behavior
        time.sleep(random.uniform(3, 6))
    
    # Add the results to your DataFrame and save to a new CSV
    tbr_list["KU_Availability"] = ku_availability
    tbr_list.to_csv("ku_checked.csv", index=False)
    
    # Close the WebDriver after processing
    driver.quit()

if __name__ == "__main__":
    main()
