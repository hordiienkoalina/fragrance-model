import requests
from bs4 import BeautifulSoup
import csv

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the webpage for {url}")
        return None

def extract_perfume_info(soup):
    perfume_info = {}
    
    # Extracting perfume name without the release year
    title_section = soup.find("h1", class_="p_name_h1")
    if title_section:
        perfume_name = title_section.find(itemprop="name").text.strip()  # Targeting only the perfume name
        perfume_info['Perfume Name'] = perfume_name
        
        brand_section = title_section.find("span", itemprop="brand")
        if brand_section:
            brand = brand_section.find(itemprop="name").text.strip()  # Ensuring only the brand name is captured
            perfume_info['Brand'] = brand

    # Extracting release year separately
    year_section = title_section.find("a", href=lambda href: href and "Release_Years" in href)
    if year_section:
        perfume_info['Release Year'] = year_section.text.strip("()")  # Removing parentheses

    notes_section = soup.find("div", class_="notes_list")
    if notes_section:
        notes = [note.get_text(strip=True) for note in notes_section.find_all("span", class_="nowrap")]
        perfume_info['Fragrance Notes'] = ", ".join(notes)

    # Adjusted perfumers extraction logic
    perfumers_section = soup.find("div", class_="w-100 mt-0-5 mb-3")
    if perfumers_section:
        perfumers = [a.text for a in perfumers_section.find_all("a", href=lambda href: "Perfumers" in href)]
        perfume_info['Perfumers'] = ", ".join(perfumers)

    rating_section = soup.find(itemprop="aggregateRating")
    if rating_section:
        perfume_info['Rating'] = rating_section.find(itemprop="ratingValue").text.strip()

    accords_section = soup.find("h2", text="Main accords").find_next_sibling("div")
    if accords_section:
        accords = [accord.get_text(strip=True) for accord in accords_section.find_all("div", class_="text-xs")]
        perfume_info['Main Accords'] = ", ".join(accords)

    # Adjusted marketing company extraction logic
    description_section = soup.find("div", class_="p_details_desc")
    if description_section:
        marketing_company_link = description_section.find("a", href=lambda href: "makers" in href)
        if marketing_company_link:
            perfume_info['Marketing Company'] = marketing_company_link.text.strip()

    return perfume_info if soup else None

# Function to read URLs from a file
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

# Path to the file containing URLs
file_path = 'data/urls_dislike.txt'
urls = read_urls_from_file(file_path)

# CSV file setup
csv_file = 'data/dislike.csv'
fieldnames = ['Perfume Name', 'Brand', 'Release Year', 'Fragrance Notes', 'Perfumers', 'Rating', 'Main Accords', 'Marketing Company']
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    
    for url in urls:
        soup = get_soup(url)
        if soup:
            perfume_info = extract_perfume_info(soup)
            if perfume_info:  # Ensure data was successfully extracted
                writer.writerow(perfume_info)
                print(f"Information about {perfume_info.get('Perfume Name', 'Unknown')} saved.")
            else:
                print(f"Failed to extract information from {url}.")
        else:
            print(f"Skipping {url} due to failed web page retrieval.")

print(f"All information has been saved to {csv_file}.")
