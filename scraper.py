import requests

from bs4 import BeautifulSoup
from product import Product
from data_saver import save_scraped_data_to_json_file, save_scraped_data_to_sqlite_db



class scraper: 

    def __init__(self, product_list, pages, HEADERS, id=1):
        self.product_list = product_list
        self.pages = pages
        self.HEADERS = HEADERS
        self.id = id

    def scrape(self):
        for product in self.product_list:
            product_list_scraped = []
            for i in range(1, self.pages):
                r = requests.get('https://www.amazon.com/s?k=' + str(product) + '&page='+ str(i), headers=self.HEADERS)
                soup = BeautifulSoup(r.content, "lxml")
                product_soup = soup.find_all("div", class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")

                if r.status_code != 200:
                    print("Request was not successful")
                else:

                    for j in range(0, len(product_soup)):
                        product_item = Product(product_soup[j])
                        print(product_item.get_product())
                        product_list_scraped.append(product_item.get_product_json())

                
            
            save_scraped_data_to_json_file(str(product), product_list_scraped)
            save_scraped_data_to_sqlite_db(self.id, str(product),  product_list_scraped)
            

        return product_list_scraped
    



