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

def check_kindle_unlimited(driver, search_url, target_author):
    try:
        driver.get(search_url)
        
        # Wait briefly for the page to load
        time.sleep(random.uniform(2, 4))

        # Grab all search results
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")

        # -- New Step: If no results, treat it as an error page --
        if not search_results:
            print(f"Oops or no results. Returning 'I am a muppet' for {search_url}")
            return "I am a muppet"

        for result in search_results:
            try:
                author_row = result.find_element(By.CSS_SELECTOR, "div.a-row.a-size-base.a-color-secondary")
                author_text = author_row.text.strip().lower()
                
                print(f"Found author row text: '{author_text}'")

                # Partial match for the author
                if target_author.lower() in author_text:
                    badges = result.find_elements(By.CSS_SELECTOR, ".apex-kindle-program-badge, .afr-limber-program-badge")
                    if badges:
                        return "Available"
                    else:
                        return "Not Available"
                    
            except NoSuchElementException:
                continue

        print(f"No matching author found on the search page for '{target_author}'.")
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
        # Keep the Books category filter
        search_url = f"https://www.amazon.com/s?k={encoded_title}+{encoded_authors}&i=stripbooks"

        # Check KU availability using Selenium, passing the author name
        availability = check_kindle_unlimited(driver, search_url, authors)
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