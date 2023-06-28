import random
import re
# GAME: https://en.wikipedia.org/wiki/Hangman_(game)

print("""################
# HANGMAN GAME #
################\n""")

def replace_spaces(guess, spaces, word):
    """ Function to replace letter placeholders 
    with correct guesses.
    Parameters:
    - guess: letter (str) that was guessed
    - spaces: placeholder underlines (_) for word letters (str)
    - word: word (str) to guess
    Returns:
    - spaces: new string of placeholders and guessed letters.
    """
    index_list = [_.start() for _ in re.finditer(guess, word)]
    # strings immutable, so convert to list
    spaces_list = list(spaces)
    for index in index_list:    
        spaces_list[index] = guess
    spaces = ''.join(spaces_list)
    return spaces

# (1) Fetch word list from .txt file
with open('words.txt', 'r') as reader:
    words = reader.read().split("\n")
    random.shuffle(words)
    word = words[random.randint(0, len(words))].upper()
    spaces = "_" * len(word)

guess_list = []
wrong_guesses = 0

# Needs 6 wrong guesses to draw the complete image
while wrong_guesses <= 6:
    # Print initial image
    with open(f'ascii_{wrong_guesses}.txt', 'r') as reader:
        print("Word to guess: " + spaces + '\n')
        print(reader.read())
        print('Guessed letters: ' + ', '.join(guess_list) + '\n')
    if wrong_guesses < 6:
        guess = input('Insert your character guess:').upper()
        if guess in guess_list:
            print('You already guessed this letter. Try another one.')
        else:
            guess_list.append(guess)
            if guess in word:
                spaces = replace_spaces(guess, spaces, word)
            else:
                wrong_guesses += 1
    else:
        print('You LOST! The word we were looking for was: ' + word.upper())
        wrong_guesses += 1