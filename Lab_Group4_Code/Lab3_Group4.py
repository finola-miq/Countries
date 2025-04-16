# CIS-117 Lab3
# Reads country_full.csv and categorizes each country to the region into new csv files
# Finola Miqailla
# Ailing Chow
# Group 4

import csv
import os
import requests
from io import StringIO

# URL of the raw CSV file from GitHub
input_file_url = 'https://raw.githubusercontent.com/finola-miq/Countries/refs/heads/main/country_full.csv'

region_data = {}  # Dictionary to hold region-wise countries

try:
    # Fetch the CSV content from the GitHub URL
    response = requests.get(input_file_url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

    # Read CSV data from the response content
    csv_content = response.text
    reader = csv.DictReader(StringIO(csv_content))

    print("Country - Region")
    print("----------------")
    for row in reader:
        country = row.get('name', '').strip()
        region = row.get('region', '').strip()

        if country and region:
            print(f"{country}, {region}")
            region_data.setdefault(region, []).append((country, region))

except requests.exceptions.RequestException as e:
    print(f"Error fetching the file from GitHub: {e}")
except csv.Error as e:
    print(f"Error reading the CSV file: {e}")

# Output directory for region-wise CSV files
output_dir = "regions_output"

try:
    os.makedirs(output_dir, exist_ok=True)
except Exception as e:
    print(f"Error creating folder: {e}")

# Write each region's data to its own CSV file
for region, countries in region_data.items():
    filename = f"{region}.csv"
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write("name,region\n")
            for country, region_name in countries:
                file.write(f"{country},{region_name}\n")
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Error writing file {filename}: {e}")
