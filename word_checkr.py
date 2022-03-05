# Test to see if comparison works
# Guess is compared to actual word and colour code for each letter is outputted

def word_comparison(guess_word):
    actual_word = "ahead"    

    comparison = []
    for i in range(len(actual_word)):
        if guess_word[i] == actual_word[i]:
            comparison.append('green')
        else:
            if guess_word[i] in actual_word:
                comparison.append('yellow')
            else:
                comparison.append('black')
    
    return comparison
