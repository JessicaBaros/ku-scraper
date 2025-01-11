import pandas as pd
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
import random # Amazon bot deterance
import time  # to add delays

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
    )
}

def get_product_page_link(search_url):
    """
    1. Fetch the Amazon search results.
    2. Parse HTML for the first product link.
    3. Return the full product link (or None if not found).
    """
    response = requests.get(search_url, headers=HEADERS)
    if response.status_code != 200:
        # Could be a captcha or other error.
        print("I am a muppet")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Common approach: look for the <a> tag that leads to the product detail page.
    # Amazon changes this frequently. Adjust the selector as needed.
    # Example: a typical product link might have these classes:
    # <a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" href="/gp/..."
    product_links = soup.select('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')

    if not product_links:
        return None

    # Get the 'href' of the first result
    partial_link = product_links[0].get("href", "")
    if not partial_link.startswith("http"):
        partial_link = "https://www.amazon.com" + partial_link

    return partial_link

def check_kindle_unlimited_on_product_page(product_url):
    """
    Visit the product page and look for <img alt="Kindle Unlimited">.
    Return "Available" or "Not Available."
    """
    if not product_url:
        return "Not Available"

    time.sleep(random.uniform(3, 6))  # Add some delay before hitting the product page
    response = requests.get(product_url, headers=HEADERS)
    if response.status_code != 200:
        # Possibly blocked or captcha again
        print("Product page blocked or error.")
        return "Not Available"

    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img", alt="Kindle Unlimited")
    if images:
        return "Available"
    else:
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
        search_url = f"https://www.amazon.com/s?k={encoded_title}+{encoded_authors}&i=digital-text" 
        # Note: adding '&i=digital-text' might help narrow results to Kindle eBooks.

        # Step 1: Get the top product page link from the search results.
        product_link = get_product_page_link(search_url)

        # Optional: Print or log for debugging
        print(f"Row {index}: {title}")
        print(f" Search URL: {search_url}")
        print(f" Product Link: {product_link}")

        # Step 2: Fetch the product detail page and check for KU badge.
        availability = check_kindle_unlimited_on_product_page(product_link)
        ku_availability.append(availability)

        print(f" => Availability: {availability}")
        print("---")

        # Add some random delay before moving to the next book
        time.sleep(random.uniform(5, 10))

    

if __name__ == "__main__":
    main()
