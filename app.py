from flask import Flask
from flask import request
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup
app = Flask(__name__)


#Acting Firefox Browser
hd = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Frontpage
@app.route("/")
def index():
    return "<p>Welcome!-->>>>http://127.0.0.1:5000/product_search?asin_codes=</p>"

#http://127.0.0.1:5000/product_search?asin_codes=
@app.route("/product_search")
def product_search():
    asin_codes = request.args.get("asin_codes")
    temp = []
    for asin_code in asin_codes.split(","):
    #Log(asin_code)
        asin_code = asin_code.strip()
        product_id = asin_code
        url = f"https://www.amazon.com.au/s?k={asin_code}"
    #Log(url)
        print(url)
        html = rq.get(url,headers=hd).text
        soup_1 = BeautifulSoup(html, 'html.parser')

        product = soup_1.select_one(f'[data-asin="{asin_code}"]')
        if product is None:
            print("continue",asin_code)
            print(soup_1)
            continue
        product_title = product.select_one("h2").text
        product_global_rating = product.select_one(".a-row.a-size-small span[aria-label]").text
        product_number_of_rating = product.select_one(".a-size-base").text

        product_price_tag = product.select_one(".a-price .a-offscreen")
        if product_price_tag is not None:
            product_price = product_price_tag.text.strip()
            product_availability = product.select_one("span.a-size-small").text
        else:
            product_price = "N/A"
            product_availability = "N/A"
        print("pricetag")

        temp.append([product_id,product_title,product_global_rating,product_number_of_rating,product_price, product_availability])

#ToReturn dict in list (dataframe.to_dict(orient="records")
    return {
        "result": pd.DataFrame(temp, columns=["Product ID", "Product Title", "Global Rating", "Number of Rating", "Price", "Availability"]).to_dict(orient='records')
    }