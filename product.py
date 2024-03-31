from bs4 import BeautifulSoup
import datetime

class Product:

    def __init__(self, product):
        self.product = product


        productSoup = BeautifulSoup(product.prettify(), "lxml")
        title = productSoup.find_all("span", class_="a-size-medium a-color-base a-text-normal")
        price = productSoup.find_all("span", class_="a-offscreen")
        rating = productSoup.find_all("span", class_="a-size-base s-underline-text")
        image = productSoup.find_all("img", class_="s-image")

        self.name = title[0].get_text().strip() if title else ''
        self.price = price[0].get_text().strip() if price else ''
        self.rating = rating[0].get_text().strip() if rating else ''
        self.image = image[0]['src'] if image else ''
        self.scrape_date = str(datetime.datetime.now())
        self.creation_date = str(datetime.datetime.now())
        self.update_date = str(datetime.datetime.now())


    def get_product(self):
        return f"Name: {self.name}\nPrice: {self.price}"
    
    def get_product_json(self):
        return {
            "name": self.name,
            "price": self.price,
            "rating": self.rating,
            "image": self.image,
            "scrape_date": self.scrape_date,
            "creation_date": self.creation_date,
            "update_date": self.update_date
        }