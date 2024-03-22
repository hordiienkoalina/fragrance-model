import requests
from bs4 import BeautifulSoup
import csv

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print("Failed to retrieve the webpage")
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

    return perfume_info

url = 'https://www.parfumo.com/Perfumes/Kilian/smoking-hot'
soup = get_soup(url)
if soup:
    perfume_info = extract_perfume_info(soup)
    csv_file = 'data/single_info.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        # Exclude 'Ranking' from the fields
        fieldnames = ['Perfume Name', 'Brand', 'Release Year', 'Fragrance Notes', 'Perfumers', 'Rating', 'Main Accords', 'Marketing Company']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(perfume_info)
    print(f"Information about {perfume_info.get('Perfume Name', 'Unknown')} saved to {csv_file}")
else:
    print("Failed to scrape the perfume details.")
