import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urljoin
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0. (compatible; FastAPI)',
    'Accept-Language': 'en-US,en;q=0.5'
}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}, Request headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response headers: {response.headers}")
    return response


@app.get("/test")
async def test_endpoint():
    response = JSONResponse(content={"message": "This is a test response"})
    return response


@app.get("/prices/{product_name:path}")
async def get_prices(product_name: str):
    logger.info(f"Fetching prices for: {product_name}")

    try:
        bestbuy_price = fetch_data_from_bestbuy(product_name)
        logger.info(f"BestBuy price fetched: {bestbuy_price}")

        walmart_price = fetch_data_from_walmart(product_name)  # Ensure you handle encoding inside the function
        logger.info(f"Walmart price fetched: {walmart_price}")

        newegg_price = fetch_data_from_newegg(product_name)
        logger.info(f"Newegg price fetched: {newegg_price}")

        return jsonable_encoder({
            "product_name": product_name,
            "BestBuy": bestbuy_price,
            "Walmart": walmart_price,
            "Newegg": newegg_price
        })

    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        traceback.print_exc()  # This will print the full traceback to the log
        return JSONResponse(status_code=500, content={"error": str(e)})


def fetch_data_from_bestbuy(product_name):
    encoded_product_name = urllib.parse.quote_plus(product_name[:90])
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={encoded_product_name}&intl=nosplash"
    logger.info(f"BestBuy URL: {url}")

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            price = soup.find("span", attrs={"aria-hidden": "true"}, string=re.compile(r'^\$'))
            link = soup.find('a', class_='link')
            product_container = soup.find('div', class_='sku-title')
            link = product_container.find('a', href=True) if product_container else None
            product_link = urljoin(url, link['href']) if link else None

            return {"price": price.text if price else "Not available", "link": product_link}

        return {"price": "No products found", "link": None}

    except requests.RequestException as e:
        logger.error(f"Error fetching data from BestBuy: {e}")
        return {"price": "Error fetching data from BestBuy.", "link": None}


def fetch_data_from_walmart(product_name):
    encoded_product_name = urllib.parse.quote_plus(product_name)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    url = f"https://www.walmart.com/search?q={encoded_product_name}"
    logger.info(f"Walmart URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            error_message = soup.find('div', class_='tc fw7 f-subheadline-m mb4 f1')

            if error_message is None:
                product_link = soup.find('div', class_='h-100 pb1-xl pr4-xl pv1 ph1',
                                         attrs={"style": "contain-intrinsic-size:198px 340px"}).find('a')['href']
                product_page_response = requests.get(product_link, headers=headers)

                if product_page_response.status_code == 200:
                    soup = BeautifulSoup(product_page_response.text, "html.parser")
                    price = soup.find('span', attrs={"itemprop": "price", "aria-hidden": "false"})
                    price_text = price.text[3:]

                    if (price_text[-3] != "."):
                        price_text = price_text[:-2] + "." + price_text[-2:]

                    return {"price": price_text.strip() if price_text else "Not available",
                            "link": product_link}

        return {"price": "No products found", "link": None}

    except requests.RequestException as e:
        logger.error(f"Error fetching data from Walmart: {e}")
        return {"price": "Error fetching data", "link": None}


def fetch_data_from_newegg(product_name):
    encoded_product_name = urllib.parse.quote_plus(product_name)

    # Manually replace the encoded characters for parentheses and double quotes if needed
    encoded_product_name = encoded_product_name.replace('%28', '(').replace('%29', ')')
    url = f"https://www.newegg.com/p/pl?d={encoded_product_name}&intl=nosplash"
    logger.info(f"Newegg URL: {url}")

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            error_message = soup.find("span", class_='result-message-error')

            if error_message is None:
                product_link = soup.find('div', class_='item-container').find('a')['href']
                product_page_response = requests.get(product_link, headers=headers)

                if product_page_response.status_code == 200:
                    soup = BeautifulSoup(product_page_response.text, "html.parser")
                    product_price = soup.find('li', class_='price-current')
                    return {"price": product_price.text if product_price else "Not available", "link": product_link}

            return {"price": "No products found", "link": None}

    except requests.RequestException as e:
        logger.error(f"Error fetching data from Newegg: {e}")
        return {"price": "Error fetching data", "link": None}


# # Example usage:
# product_name = "Sony XR85X93L 85\" 4K Mini LED Smart Google TV with PS5 Features (2023)"
# product_name = "HP - Envy 2-in-1 14\" Full HD Touch-Screen Laptop - Intel Core 7 - 16GB Memory - 512GB SSD -Natural Silver"
#product_name = "Sony - WF-C700N Truly Wireless Noise Canceling In-Ear Headphones - Sage"
#product_name = "Barakkat Rouge 540 by Fragrance World EDP Spray 3.4 oz For Women"
#product_name = "33234454"