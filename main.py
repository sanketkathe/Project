import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    description_element = soup.find('div', id='productDescription')
    description = description_element.text.strip() if description_element else 'N/A'

    asin_element = soup.find('th', text='ASIN')
    asin = asin_element.find_next('td').text if asin_element else 'N/A'

    product_description_element = soup.find('h2', class_='a-size-mini')
    product_description = product_description_element.find_next('span').text.strip() if product_description_element else 'N/A'

    manufacturer_element = soup.find('a', id='bylineInfo')
    manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

    return description, asin, product_description, manufacturer


base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
num_pages = 20

with open('product_details.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
    csv_writer = csv.writer(csv_output_file)
    csv_writer.writerow(['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])



    for page_num in range(1, num_pages + 1):
        page_url = f"{base_url}&page={page_num}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_containers = soup.find_all('div', class_='s-result-item')

        for container in product_containers:
            product_url_element = container.find('a', class_='a-link-normal')
            if product_url_element:
                product_url = "https://www.amazon.in" + product_url_element['href']

                product_name_element = container.find('span', class_='a-text-normal')
                product_name = product_name_element.text if product_name_element else 'N/A'

                product_price_element = container.find('span', class_='a-offscreen')
                product_price = product_price_element.text if product_price_element else 'N/A'

                rating_element = container.find('span', class_='a-icon-alt')
                rating = rating_element.text.split()[0] if rating_element else 'N/A'

                reviews_element = container.find('span', class_='a-size-base')
                num_reviews = reviews_element.text.replace(',', '') if reviews_element else '0'

                if product_url != 'N/A':
                    description, asin, product_description, manufacturer = scrape_product_details(product_url)
                else:
                    description = 'N/A'
                    asin = 'N/A'
                    product_description = 'N/A'
                    manufacturer = 'N/A'

                csv_writer.writerow([product_url, description, asin, product_description, manufacturer])

            time.sleep(1)

    csv_output_file.close()

    print("Scraping and writing to CSV completed.")

