from dotenv import load_dotenv
from word_checkr import word_comparison
import os
import psycopg
import random
import urllib.parse as up

load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["ELPHNT_DB_URL"])

class WordleQuery:
    def __init__(self) -> None:
        self.DB_USER = url.username
        self.DB_HOST = url.hostname
        self.DB_PASS = url.password
        self.DB_PORT = os.environ["DB_PORT"]
        self.DB_NAME = url.path[1:]
        self.WORDLE_LENGTH = 5

        self.green_letters = ['_', '_', '_', '_', '_'] # Green letters initially set to dashes
        self.yellow_letters = {} # Yellow letters set as dictionary to store letter and positions they occupy
        self.black_letters = [] # Black letters put in a list
        self.first = False
        self.word = ""

    def first_guess(self):
        with psycopg.connect(dbname=self.DB_NAME, user=self.DB_USER, host=self.DB_HOST, password=self.DB_PASS) as conn:
            with conn.cursor() as cur:
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
                self.first = True
                self.word = guess_word
            conn.commit()

    def subseq_guess(self, comparison):
        if not self.first:
            self.first_guess()

        with psycopg.connect(dbname=self.DB_NAME, user=self.DB_USER, host=self.DB_HOST, password=self.DB_PASS) as conn:
            with conn.cursor() as cur:
                if comparison.count("green") < 5:
                    for i in range(self.WORDLE_LENGTH):
                        if comparison[i] == 'green':
                            self.green_letters[i] = self.word[i]
                        elif comparison[i] == 'yellow':
                            self.yellow_letters[self.word[i]] = i
                        else:
                            self.black_letters.append(self.word[i])

                # Content of green, yellow, and black letters determine the amount of nesting to occur in query
                    nested_query = 'wordle'
                    
                    green_word = ''.join(self.green_letters)
                    if green_word != '_____':
                        nested_query = f'''
                            (SELECT *
                            FROM {nested_query}
                            WHERE word LIKE '{green_word}') AS green_subq
                        '''

                    if len(self.yellow_letters) != 0:
                        yellow_words = self.yellow_letter_words()
                        yellow_words = ', '.join(yellow_words)
                        nested_query = f'''
                            (SELECT *
                            FROM {nested_query}
                            WHERE word NOT LIKE ALL(ARRAY[{yellow_words}])) AS yllw_subq
                        '''

                    if len(self.black_letters) != 0:
                        black_words = self.black_letter_words()
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

                    result_count = len(db_result)-1
                    if result_count != 0:
                        guess_id = random.randint(0, result_count)
                        guess_word = db_result[guess_id][0]
                    else:
                        guess_word = db_result[result_count][0]

                    self.word = guess_word

            conn.commit()


    def yellow_letter_words(self):
        yllw_wrd_lst = []
        for key, value in self.yellow_letters.items():
            yllw_wrd = ''
            for i in range(5):
                if value == i:
                    yllw_wrd += key
                else:
                    yllw_wrd += '_'
            yllw_wrd_lst.append(yllw_wrd)

        yllw_wrd_lst = [f"'{i}'" for i in yllw_wrd_lst]

        return yllw_wrd_lst

    def black_letter_words(self):
        blck_wrd_lst = []
        for i in self.black_letters:
            if not(i in self.green_letters or i in list(self.yellow_letters.keys())):
                blck_wrd = f"{i}____"
                blck_wrd_lst.append(blck_wrd)
                for j in range(1, 5):
                    blck_wrd_lst.append(blck_wrd[j:] + blck_wrd[:j])

        blck_wrd_lst = [f"'{i}'" for i in blck_wrd_lst]
        
        return blck_wrd_lst      
