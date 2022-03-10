## WordlePlayerOne
A bot that plays Wordle.

The bot plays Wordle using a PostgreSQL database containing 8939 5-letter words.
<br>
The first try involves picking a word at random from the database. This word is compared to the actual word being guessed.
<br>
The comparison returns
'green': if the letter is part of the actual word and in its correct position
'yellow': if the letter is part of the actual word but not in it correct position
'black': if the letter is not part of the actual word.

Based on this output queries are constructed to narrow down the database till the actual word is correctly picked(i.e. comparison returns a 'green' for all five positions).

The 'green' subquery simply compares all words in the database to any word that matches the pattern.
<br>
The 'yellow' subquery matches the words that have the letters in positions other than the previously guessed positions.
<br>
The 'black' subquery matches removes all words that possess any occurence of the letters.


