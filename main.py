from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

app = FastAPI()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.',
    'Accept-Language': 'en-US,en;q=0.5'
}

@app.get("/prices/{product_name}")
async def get_prices(product_name: str):
    encoded_product_name = urllib.parse.quote_plus(product_name)
    bestbuy_price = fetch_data_from_bestbuy(encoded_product_name)
    walmart_price = fetch_data_from_walmart(encoded_product_name)  # Ensure you handle encoding inside the function
    newegg_price = fetch_data_from_newegg(encoded_product_name)

    return {
        "product_name": product_name,
        "BestBuy": bestbuy_price,
        "Walmart": walmart_price,
        "Newegg": newegg_price
    }

# first here is a simple python program that fetchs the data for the const = “Sony XR85X93L 85" 4K Mini LED Smart Google TV with PS5 Features (2023)”
# global bestbuy_product_price, walmart_product_price, newegg_product_price

def fetch_data_from_bestbuy(product_name):
    encoded_product_name = urllib.parse.quote_plus(product_name[:90])
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={encoded_product_name}&intl=nosplash"
    # print(url)

    try:
        page_to_scrape = requests.get(url, headers=headers)

        # Check if the request was successful
        if page_to_scrape.status_code == 200:
            soup = BeautifulSoup(page_to_scrape.text, "html.parser")
            price = soup.find("span", attrs={"aria-hidden": "true"}, string=re.compile(r'^\$'))
            if price:
                return price.text

        return "No products found in search results."
    except requests.RequestException:
        return "Error fetching data from BestBuy."


def fetch_data_from_walmart(product_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    url = f"https://www.walmart.com/search?q={encoded_product_name}"

    try:
        page_to_scrape = requests.get(url, headers=headers)

        if page_to_scrape.status_code == 200:
            soup = BeautifulSoup(page_to_scrape.text, "html.parser")
            error_message = soup.find('div', class_='tc fw7 f-subheadline-m mb4 f1')

            if error_message is None:
                product_link = soup.find('div', class_='h-100 pb1-xl pr4-xl pv1 ph1',
                                         attrs={"style": "contain-intrinsic-size:198px 340px"}).find('a')['href']
                product_page_response = requests.get(product_link, headers=headers)

                if product_page_response.status_code == 200:
                    soup = BeautifulSoup(product_page_response.text, "html.parser")
                    price_text = soup.find('span', attrs={"itemprop": "price", "aria-hidden": "false"})
                    return price_text.text.strip()

        return "No products found in search results."

    except requests.RequestException:
        return "Error fetching data from Walmart."


def fetch_data_from_newegg(product_name):
    encoded = urllib.parse.quote_plus(product_name)

    # Manually replace the encoded characters for parentheses and double quotes if needed
    encoded_product_name = encoded.replace('%28', '(').replace('%29', ')')
    url = f"https://www.newegg.com/p/pl?d={encoded_product_name}&intl=nosplash"
    print(url)
    page_to_scrape = requests.get(url, headers=headers)

    # Check if the request was successful
    if page_to_scrape.status_code == 200:
        # Find the HTML element representing the first product listing
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")  
        error_message = soup.find("span", class_='result-message-error')

        if error_message is None:
            product_link = soup.find('div', class_='item-container').find('a')['href']
            product_page_response = requests.get(product_link, headers=headers)

            if product_page_response.status_code == 200:
                soup = BeautifulSoup(product_page_response.text, "html.parser")
                product_price = soup.find('li', class_='price-current')
                return product_price.text

        return "No products found in search results."

    return "Error fetching data from Newegg."


# Example usage:
#product_name = "Sony XR85X93L 85\" 4K Mini LED Smart Google TV with PS5 Features (2023)"
product_name = "HP - Envy 2-in-1 14\" Full HD Touch-Screen Laptop - Intel Core 7 - 16GB Memory - 512GB SSD -Natural Silver"
#product_name = "Sony - WF-C700N Truly Wireless Noise Canceling In-Ear Headphones - Sage"
#product_name = "Barakkat Rouge 540 by Fragrance World EDP Spray 3.4 oz For Women"
#product_name = "33234454"


# #data_from_bestbuy = fetch_data_from_bestbuy(product_name)
# data_from_walmart = fetch_data_from_walmart(encoded_product_name)
# #data_from_newegg = fetch_data_from_newegg(product_name)

