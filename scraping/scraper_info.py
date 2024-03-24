import csv
import os
import requests
import time
from bs4 import BeautifulSoup
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError

### ----- SETUP ----- ###

# Rate limiting and Parallelisation
MAX_WORKERS = 5
SLEEP_TIME = 2
MIN_SLEEP_TIME = 1
MAX_SLEEP_TIME = 5

def get_soup(url, retry_times=3):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for _ in range(retry_times):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
            return BeautifulSoup(response.text, 'html.parser')
        except ConnectionError:
            print(f"Connection error for {url}. Retrying...")
            time.sleep(random.uniform(1, 3))  # Random delay before retrying
    print(f"Failed to retrieve the webpage for {url} after {retry_times} attempts.")
    return None

### ----- IMAGES ----- ###

IMAGE_DIR = 'images_v2'

def download_image(img_url, save_path):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(img_url, headers=headers)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded image to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {img_url}. Error: {e}")

### ----- PERFUME DATA ----- ###

def extract_perfume_data(soup):
    if not soup:
        return None

    perfume_info = {}

    # Perfume Name
    title_section = soup.find("h1", class_="p_name_h1")
    if title_section:
        perfume_info['Perfume Name'] = title_section.text.strip()

    # Brand 
    brand_section = soup.find("span", itemprop="name")
    if brand_section:
        perfume_info['Brand'] = brand_section.text.strip()

    # Release Year 
    release_year_section = soup.find("span", class_="label_a")
    if release_year_section:
        perfume_info['Release Year'] = release_year_section.text.strip()

    # Fragrance Notes 
    notes_section = soup.find_all("span", class_="nowrap pointer")
    if notes_section:
        notes = [note.text.strip() for note in notes_section]
        perfume_info['Fragrance Notes'] = ", ".join(notes)

    # # Perfumers 
    # perfumers_section = soup.find("div", class_="perfumers")
    # if perfumers_section:
    #     perfumers = [perfumer.text.strip() for perfumer in perfumers_section.find_all("a")]
    #     perfume_info['Perfumers'] = ", ".join(perfumers)

    # Rating 
    rating_section = soup.find_all("span", itemprop="ratingValue")
    if rating_section:
        ratings = [float(rating.text.strip()) for rating in rating_section]
        average_rating = sum(ratings) / len(ratings) if ratings else None
        perfume_info['Rating'] = average_rating

    # Main Accords 
    accords_section = soup.find("div", class_="accords")
    if accords_section:
        accords = [accord.text.strip() for accord in accords_section.find_all("div", class_="text-xs grey")]
        perfume_info['Main Accords'] = ", ".join(accords)

    # Marketing Company 
    # marketing_section = soup.find("div", class_="marketing")
    # if marketing_section:
    #     marketing_company = marketing_section.text.strip()
    #     perfume_info['Marketing Company'] = marketing_company

    # Bottle Image
    img_tag = soup.find('img', {'class': 'p-main-img'})
    if img_tag and 'src' in img_tag.attrs:
        img_url = img_tag['src']
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)
        filename = perfume_info.get('Perfume Name', 'Unknown').replace('/', '_').replace('\\', '_').replace(' ', '_') + '.jpg'
        save_path = os.path.join(IMAGE_DIR, filename)
        download_image(img_url, save_path)
        perfume_info['Image Path'] = save_path

    return perfume_info

# Function to read URLs from a file
def read_urls_from_file(file_path, start_line=0):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls[start_line:]

# Path to the file containing URLs
file_path = 'data/popular_brands.txt'
start_line = 4073
urls = read_urls_from_file(file_path, start_line)

# CSV file setup
csv_file = 'data/popular_perfumes.csv'
fieldnames = ['Perfume Name', 'Brand', 'Release Year', 'Fragrance Notes', 'Rating', 'Main Accords', 'Image Path']

# Open the file in append mode ('a') instead of write mode ('w')
with open(csv_file, 'a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if start_line == 0:  # Only write the header if this is the first line
        writer.writeheader()
    
    for url in urls:
        soup = get_soup(url)
        if soup:
            perfume_info = extract_perfume_data(soup)
            if perfume_info:  # Ensure data was successfully extracted
                writer.writerow(perfume_info)
                print(f"Information about {perfume_info.get('Perfume Name', 'Unknown')} saved.")
            else:
                print(f"Failed to extract information from {url}.")
        else:
            print(f"Skipping {url} due to failed web page retrieval.")
        
        # Add delay here
        time.sleep(random.uniform(MIN_SLEEP_TIME, MAX_SLEEP_TIME))

print(f"All information has been saved to {csv_file}.")