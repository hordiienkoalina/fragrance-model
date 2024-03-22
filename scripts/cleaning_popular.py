import pandas as pd
import re

# Load the CSV file
df = pd.read_csv('data/popular_brands.csv')

# Define a function to extract the year from the perfume name
def extract_year(perfume_name):
    perfume_name = str(perfume_name)
    matches = re.findall(r'\b\d{4}\b', perfume_name)
    return matches[-1] if matches else None

# Apply the function to the 'Perfume Name' column
df['Year'] = df['Perfume Name'].apply(extract_year)

# Drop the old 'Release Year' column
df = df.drop('Release Year', axis=1)

# Rename the new 'Year' column to 'Release Year'
df = df.rename(columns={'Year': 'Release Year'})

# Drop the 'Main Accords' column
df = df.drop('Main Accords', axis=1)

# Save the cleaned DataFrame to a new CSV file
df.to_csv('data/cleaned_popular_brands.csv', index=False)