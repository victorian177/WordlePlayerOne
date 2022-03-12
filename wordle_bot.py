from seleniumbase import BaseCase
from query import WordleQuery
from word_checkr import word_comparison
import time

class WordleBot(BaseCase):
    def test_wordle(self):
        query = WordleQuery()

        self.open("https://www.nytimes.com/games/wordle/index.html")
        self.click("game-app::shadow game-theme-manager div#game game-modal::shadow game-icon")
        time.sleep(2)
        kybrd = "game-app::shadow game-theme-manager div#game game-keyboard::shadow div#keyboard div.row "


        # First guess
        query.first_guess()
        for i in query.word:
            self.click(kybrd + f'button[data-key="{i}"]')
            time.sleep(1)

        self.click(kybrd + f'button[data-key="↵"]')
        time.sleep(5)

        # Subsequent guesses: wordle only allows for 6 guesses
        for i in range(5):
            row = f'game-app::shadow game-row[letters="{query.word}"]::shadow '
            tile = row + "game-tile:nth-of-type(%s)"
            self.wait_for_element(tile % "5" + '::shadow [data-state*="e"]')
            letter_status = []
            for i in range(1, 6):
                letter_eval = self.get_attribute(tile % str(i), "evaluation")
                letter_status.append(letter_eval)

            if letter_status.count("correct") == 5:
                break

            comparison = word_comparison(letter_status)
            query.subseq_guess(comparison=comparison)

            for i in query.word:
                self.click(kybrd + f'button[data-key="{i}"]')
                time.sleep(1)

            self.click(kybrd + f'button[data-key="↵"]')
            time.sleep(5)

        time.sleep(10)
