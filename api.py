import sqlite3
import uuid

from fastapi import Request, FastAPI

from scraper import scraper


HEADERS = ({'User-Agent':
           'Mozilla/5.0 (X11; Windows x86_64) ' +
           'AppleWebKit/537.36 (KHTML, like Gecko)' + 
                    'Chrome/44.0.2403.157 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})


app = FastAPI()

# function to generate a random string of length 10

def random_string():
    return str(uuid.uuid4())[:6]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/fetch_query")
async def create_request(request: Request):
    

    # Store the request ID in the SQLite database
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS requests 
                   (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS query_id 
                   (
                        id INTEGER NOT NULL,
                        query TEXT NOT NULL,
                        PRIMARY KEY (id, query)
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS product 
                   (
                        id INTEGER NOT NULL,
                        query TEXT NOT NULL,
                        productId INTEGER PRIMARY KEY AUTOINCREMENT,
                        Title TEXT,
                        Price TEXT,
                        Rating TEXT,
                        Image TEXT
                   )""")


    cursor.execute("INSERT INTO requests (name) VALUES (?)", ( random_string(),))

    generated_id = cursor.lastrowid


    queries = await request.json()

 

    for query in queries:
        cursor.execute("""
                       INSERT INTO query_id (id, query) VALUES (?, ?)
                       """, (generated_id, query))
        
    conn.commit()
    conn.close()
    
    
    product_list = scraper(queries, 20, HEADERS, generated_id ).scrape()

    
    return {"request_id": generated_id}


@app.get("/fetch_query/{request_id}")
def fetch_query(request_id: int):
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    cursor.execute("SELECT query FROM query_id WHERE id = ?", (request_id,))
    queries = cursor.fetchall()

    cursor.execute("SELECT * FROM product WHERE id = ?", (request_id,))
    products = cursor.fetchall()

    conn.close()
    
    return {"products":products, "queries": queries}