import requests
from bs4 import BeautifulSoup
import urllib
import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.',
    'Accept-Language': 'en-US,en;q=0.5'
}

# first here is a simple python program that fetchs the data for the const = “Sony XR85X93L 85" 4K Mini LED Smart Google TV with PS5 Features (2023)”
global bestbuy_product_price, walmart_product_price, newegg_product_price

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
                bestbuy_product_price = price.text
                print("bestbuy's product price is: " + str(bestbuy_product_price))
            else:
                print("No products found in search results.")
    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")


def fetch_data_from_walmart(product_name):
    url = f"https://www.walmart.com/search?q={encoded_product_name}"
    print(url)

    try:
        page_to_scrape = requests.get(url, headers=headers)

        # Check if the request was successful
        if page_to_scrape.status_code == 200:
            soup = BeautifulSoup(page_to_scrape.text, "html.parser")
            price_text = soup.find('div', class_='mr1 mr2-xl b black green lh-copy f5 f4-l', attrs={"aria-hidden": "true"})
            price_text = price_text.text[3:]
            # Insert a dot before the last two characters
            walmart_product_price = f"{price_text[:-2]}.{price_text[-2:]}"

            if walmart_product_price:
                print("walmart's product price is: " + str(walmart_product_price))
            else:
                print("No products found in search results.")
    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")    

    #prices = soup.find_all("div", class_="priceView-hero-price priceView-customer-price", attrs={"data-testid": "customer-price"})



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
#product_name = "Sony XR85X93L 85\" 4K Mini LED Smart Google TV with PS5 Features (2023)"
#product_name = "HP - Envy 2-in-1 14\" Full HD Touch-Screen Laptop - Intel Core 7 - 16GB Memory - 512GB SSD -Natural Silver"
product_name = "Sony - WF-C700N Truly Wireless Noise Canceling In-Ear Headphones - Sage"

encoded_product_name = urllib.parse.quote_plus(product_name)

# data_from_bestbuy = fetch_data_from_bestbuy(product_name)
data_from_walmart = fetch_data_from_walmart(encoded_product_name)
# data_from_newegg = fetch_data_from_newegg(encoded_product_name)


print("Script ended")