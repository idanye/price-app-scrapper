import requests
from bs4 import BeautifulSoup
import urllib
import re


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

        if page_to_scrape.status_code == 200:
            soup = BeautifulSoup(page_to_scrape.text, "html.parser")
            error_message = soup.find('div', class_='tc fw7 f-subheadline-m mb4 f1') # does not find the product
            #print(soup)

            if error_message is not None:
                print("Walmart found 0 items that match: " + product_name)
            else:
                product_link = soup.find('div', class_='h-100 pb1-xl pr4-xl pv1 ph1', attrs={"style":"contain-intrinsic-size:198px 340px"}).find('a')['href']
                product_page_response = requests.get(product_link, headers=headers)
                #print(product_link)
            
                if product_page_response.status_code == 200:
                    soup = BeautifulSoup(product_page_response.text, "html.parser")
                    price_text = soup.find('span', attrs={"itemprop":"price", "aria-hidden": "false"})
                    walmart_product_price = price_text.text.strip()
                    print("walamart's price: " + walmart_product_price)
                else:
                    print("product does not found in Walmart")

    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}") 


def fetch_data_from_newegg(product_name):
    encoded = urllib.parse.quote_plus(product_name)
    # Manually replace the encoded characters for parentheses and double quotes if needed
    encoded_product_name = encoded.replace('%28', '(').replace('%29', ')')
    url = f"https://www.newegg.com/p/pl?d={encoded_product_name}&intl=nosplash"
    print(url)
    page_to_scrape = requests.get(url, headers=headers)

    # Check if the request was successful
    if page_to_scrape.status_code == 200:
        print("Successfully fetched the webpage")
        # Find the HTML element representing the first product listing
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")  
        error_message = soup.find("span", class_='result-message-error')

        if error_message is not None:
            print("newegg found 0 items that match: " + product_name)
        else:
            product_link = soup.find('div', class_='item-container').find('a')['href']
            product_page_response = requests.get(product_link, headers=headers)
            print(product_link)
        
            if product_page_response.status_code == 200:
                soup = BeautifulSoup(product_page_response.text, "html.parser")
                product_price = soup.find('li', class_='price-current')
                print(product_price.text)
            else:
                print("product does not found in newegg")

    else:
        print("Failed to fetch the webpage")


# Example usage:
product_name = "Sony XR85X93L 85\" 4K Mini LED Smart Google TV with PS5 Features (2023)"
#product_name = "HP - Envy 2-in-1 14\" Full HD Touch-Screen Laptop - Intel Core 7 - 16GB Memory - 512GB SSD -Natural Silver"
#product_name = "Sony - WF-C700N Truly Wireless Noise Canceling In-Ear Headphones - Sage"
#product_name = "Barakkat Rouge 540 by Fragrance World EDP Spray 3.4 oz For Women"
#product_name = "33234454"

encoded_product_name = urllib.parse.quote_plus(product_name)

#data_from_bestbuy = fetch_data_from_bestbuy(product_name)
data_from_walmart = fetch_data_from_walmart(encoded_product_name)
#data_from_newegg = fetch_data_from_newegg(product_name)

