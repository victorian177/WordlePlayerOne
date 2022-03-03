from dotenv import load_dotenv
from word_checkr import word_comparison
import os
import psycopg
import random
import sqlalchemy
import urllib.parse as up

load_dotenv()

def black_letter_words(lttr_lst: list):
    blck_wrd_lst = []
    for i in lttr_lst:
        blck_wrd = f"{i}____"
        blck_wrd_lst.append(blck_wrd)
        for j in range(1, 5):
            blck_wrd_lst.append(blck_wrd[j:] + blck_wrd[:j])

    blck_wrd_lst = [f"'{i}'" for i in blck_wrd_lst]
    
    return blck_wrd_lst

def yellow_letter_words(yllw_lttrs):
    yllw_wrd_lst = []
    for key, value in yllw_lttrs.items():
        yllw_wrd = ''
        for i in range(5):
            if value == i:
                yllw_wrd += key
            else:
                yllw_wrd += '_'
        yllw_wrd_lst.append(yllw_wrd)

    yllw_wrd_lst = [f"'{i}'" for i in yllw_wrd_lst]

    return yllw_wrd_lst
        
    

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["ELPHNT_DB_URL"])

DB_USER = url.username
DB_HOST = url.hostname
DB_PASS = url.password
DB_PORT = os.environ["DB_PORT"]
DB_NAME = url.path[1:]

with psycopg.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASS) as conn:
    with conn.cursor() as cur:

        '''Word finder'''

        green_letters = ['_', '_', '_', '_', '_']
        yellow_letters = {}
        black_letters = []

        # First guess
        cur.execute('''
            SELECT COUNT(*) FROM wordle;
        ''')
        db_count = cur.fetchall()[0][0]

        guess_id = random.randint(1, db_count)

        cur.execute(f''' 
            SELECT word
            FROM wordle
            WHERE id = {guess_id}
        ''')

        guess_word = cur.fetchall()[0][0]
        comparison = word_comparison(guess_word)

        while comparison.count('green') < 5:
            print(guess_word)
            for i in range(len(guess_word)):
                if comparison[i] == 'green':
                    green_letters[i] = guess_word[i]
                elif comparison[i] == 'yellow':
                    yellow_letters[guess_word[i]] = i
                else:
                    black_letters.append(guess_word[i])

            nested_query = 'wordle'
            
            green_word = ''.join(green_letters)
            if green_letters != '_____':
                nested_query = f'''
                    (SELECT *
                    FROM {nested_query}
                    WHERE word LIKE '{green_word}') AS green_subq
                '''

            if len(yellow_letters) != 0:
                yellow_words = yellow_letter_words(yellow_letters)
                yellow_words = ', '.join(yellow_words)
                nested_query = f'''
                    (SELECT *
                    FROM {nested_query}
                    WHERE word NOT LIKE ALL(ARRAY[{yellow_words}])) AS yllw_subq
                '''

            if len(black_letters) != 0:
                black_words = black_letter_words(black_letters)
                black_words = ', '.join(black_words)
            else:
                black_words = '12345'

            query = f'''
                SELECT word
                FROM {nested_query}
                WHERE word NOT LIKE ALL(ARRAY[{black_words}]);
            '''

            cur.execute(query)
            db_result = cur.fetchall()
            
            guess_id = random.randint(1, len(db_result)-1)
            guess_word = db_result[guess_id][0]

            comparison = word_comparison(guess_word)

        print(comparison)

    conn.commit()
