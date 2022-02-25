import psycopg 

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
with open("wordlelist.txt") as doc:
    word_text = doc.read()
word_list = word_text.splitlines();

DB_NAME = "wordle_db"
DB_USER = "wordle_player_one"
DB_HOST = "localhost"
DB_PASS = "1234"
DB_PORT = 5432

with psycopg.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASS, port=DB_PORT) as conn:
    with conn.cursor() as cur:

        # cur.execute('''
        #     CREATE TABLE IF NOT EXISTS wordle (
        #         id serial PRIMARY KEY,
        #         word VARCHAR(5) );
        #     ''')
        # cur.execute('''
        #         INSERT INTO wordle (id, word) VALUES (%s, %s)
        #     ''', (1, 'aahed'))
        # for indx in range(len(word_list[1:])):
        #     cur.execute('''
        #         INSERT INTO wordle (id, word) VALUES (%s, %s)
        #     ''', (indx + 2, word_list[indx + 1]))

        conn.commit()