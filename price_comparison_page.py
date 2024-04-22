import requests
from bs4 import BeautifulSoup
import urllib

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.',
    'Accept-Language': 'en-US,en;q=0.5'
}

print("Script started")

# first here is a simple python program that fetchs the data for the const = “Sony XR85X93L 85" 4K Mini LED Smart Google TV with PS5 Features (2023)”

def fetch_data_from_bestbuy(product_name):
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={encoded_product_name}"
    print(url)
    page_to_scrape = requests.get(url, headers=headers)

    # Check if the request was successful
    if page_to_scrape.status_code == 200:
        print("Successfully fetched the webpage")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        prices = soup.find_all("div", class_="priceView-hero-price priceView-customer-price", attrs={"data-testid": "customer-price"})
        if prices:
            # Extract the price text from the first price container found
            first_price = prices[0].find("span", attrs={"aria-hidden": "true"}).get_text().strip()
            print(f"Price of the first product: {first_price}")
        else:
            print("No products found in search results.")
    else:
        print("Failed to fetch the webpage")


def fetch_data_from_walmart(product_name):
    url = f"https://www.walmart.com/search?q={encoded_product_name}"
    print(url)
    page_to_scrape = requests.get(url, headers=headers)

    # Check if the request was successful
    if page_to_scrape.status_code == 200:
        print("Successfully fetched the webpage")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        prices = soup.find_all("div", class_="priceView-hero-price priceView-customer-price", attrs={"data-testid": "customer-price"})
        if prices:
            # Extract the price text from the first price container found
            first_price = prices[0].find("span", attrs={"aria-hidden": "true"}).get_text().strip()
            print(f"Price of the first product: {first_price}")
        else:
            print("No products found in search results.")
    else:
        print("Failed to fetch the webpage")


def fetch_data_from_newegg(product_name):
    url = f"https://www.newegg.com/p/pl?d={encoded_product_name}"
    print(url)

    page_to_scrape = requests.get(url, headers=headers)

    # Check if the request was successful
    if page_to_scrape.status_code == 200:
        print("Successfully fetched the webpage")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        prices = soup.find_all("div", class_="priceView-hero-price priceView-customer-price", attrs={"data-testid": "customer-price"})
        if prices:
            # Extract the price text from the first price container found
            first_price = prices[0].find("span", attrs={"aria-hidden": "true"}).get_text().strip()
            print(f"Price of the first product: {first_price}")
        else:
            print("No products found in search results.")
    else:
        print("Failed to fetch the webpage")


# Example usage:
product_name = "Sony XR85X93L 85\" 4K Mini LED Smart Google TV with PS5 Features (2023)"
encoded_product_name = urllib.parse.quote_plus(product_name)

data_from_bestbuy = fetch_data_from_bestbuy(product_name)
data_from_walmart = fetch_data_from_walmart(product_name)
data_from_newegg = fetch_data_from_newegg(product_name)

print("Script ended")