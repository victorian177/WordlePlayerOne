from dotenv import load_dotenv
import os
import psycopg
import urllib.parse as up

load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["ELPHNT_DB_URL"])
txt_file_name = "wordlelist.txt"

with open(f"{txt_file_name}") as doc:
    word_text = doc.read()
word_list = word_text.splitlines()

DB_USER = url.username
DB_HOST = url.hostname
DB_PASS = url.password
DB_PORT = os.environ["DB_PORT"]
DB_NAME = url.path[1:]

with psycopg.connect(dbname=DB_NAME,
    user=DB_USER, 
    host=DB_HOST, 
    password=DB_PASS) as conn:
    with conn.cursor() as cur:
        '''Database creation and management'''

        # cur.execute('''
        #     CREATE TABLE IF NOT EXISTS wordle (
        #         id serial PRIMARY KEY,
        #         word VARCHAR(5));
        #     ''')

        # for indx in range(len(word_list)):
        #     cur.execute('''
        #         INSERT INTO wordle (id, word) VALUES (%s, %s);
        #     ''', (indx + 1, word_list[indx]))
        #     print(f"ENTERED {indx}")