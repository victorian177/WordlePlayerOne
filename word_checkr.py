# Guess is compared to results from Wordle site and colour codes for each letter

def word_comparison(result_from_guess):  
    WORDLE_LENGTH = 5

    comparison = []
    for i in range(WORDLE_LENGTH):
        if result_from_guess[i] == "correct":
            comparison.append('green')
        elif result_from_guess[i] == "present":
            comparison.append('yellow')
        else:
            comparison.append('black')
    
    return comparison
