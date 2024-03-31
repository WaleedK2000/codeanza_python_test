import json
import sqlite3

def save_scraped_data_to_json_file(filename, data):
    with open( 'output/' + filename + '.json', 'w') as f:
        json.dump(data, f)


def save_scraped_data_to_sqlite_db(id, query, data):
    

    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS product
                     (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            query TEXT NOT NULL,
                            productId INTEGER PRIMARY KEY AUTOINCREMENT,
                            Title TEXT,
                            Price TEXT,
                            Rating TEXT,
                            Image TEXT
                     )""")
    
    for product in data:
        cursor.execute("""
                       INSERT INTO product (id, query, Title, Price, Rating, Image)
                            VALUES (?, ?, ?, ?, ?, ?)
                       """, 
                       (id, query, product['name'], product['price'], product['rating'], product['image']))
        

    conn.commit()
    conn.close()
