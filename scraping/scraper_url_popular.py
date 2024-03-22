import time
import os
import random
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

# Constants
USER_AGENT = {'User-Agent': 'Mozilla/5.0'}
SLEEP_TIME = 2  # seconds to wait between requests
CHECKPOINT_FREQUENCY = 500  # URLs
SAVE_DIR = "urls"  # Directory to save text files
EXCLUDE_URLS = ["https://www.parfumo.com/Perfumes/Dupes"]  # URLs to exclude from saving

# Ensure SAVE_DIR exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Setup session with retry strategy
session = requests.Session()
retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def get_soup(url):
    time.sleep(SLEEP_TIME)  # Respect rate limiting
    response = session.get(url, headers=USER_AGENT)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve webpage: {url}")
        return None

def get_brand_urls(letter_page_soup):
    brand_links = letter_page_soup.select('a[href*="/Perfumes/"]:not([href*="?current_page="])')
    return [link['href'] for link in brand_links if not link['href'].endswith('/Perfumes')]

def get_perfume_urls(brand_url):
    soup = get_soup(brand_url)
    if soup:
        perfume_links = set(soup.select('a[href^="https://www.parfumo.com/Perfumes/"]:not([href*="?current_page="])'))
        # Filter out non-specific and excluded URLs
        specific_perfume_urls = {link['href'] for link in perfume_links if not link['href'].endswith(brand_url.split('/')[-1]) and link['href'] not in EXCLUDE_URLS}
        return list(specific_perfume_urls)
    return []

def save_urls_to_file(urls, file_name):
    full_path = os.path.join(SAVE_DIR, file_name)
    with open(full_path, 'a') as file:
        for url in urls:
            file.write(url + '\n')

def scrape_and_save():
    popular_brands_url = "https://www.parfumo.com/Popular_Brands"
    popular_brands_soup = get_soup(popular_brands_url)
    if not popular_brands_soup:
        return

    brand_urls = get_brand_urls(popular_brands_soup)
    urls_checkpoint = []

    for brand_url in brand_urls:
        perfume_urls = get_perfume_urls(brand_url)
        urls_checkpoint.extend(perfume_urls)
        
        if len(urls_checkpoint) >= CHECKPOINT_FREQUENCY:
            save_urls_to_file(urls_checkpoint, "popular_brands.txt")
            urls_checkpoint = []  # Reset checkpoint buffer

        time.sleep(random.uniform(1, 3))  # Add delay between requests

    if urls_checkpoint:
        save_urls_to_file(urls_checkpoint, "popular_brands.txt")
        print(f"Saved {len(urls_checkpoint)} perfume URLs to popular_brands.txt")

if __name__ == "__main__":
    scrape_and_save()