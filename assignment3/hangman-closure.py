def make_hangman(secret_word):
    guesses = []
    
    def hangman_closure(letter):
        guesses.append(letter)
        display = ''.join([char if char in guesses else '_' for char in secret_word])
        print(display)
        return all(c in guesses for c in secret_word)
    
    return hangman_closure

if __name__ == "__main__":
    word = input("Enter the secret word: ").lower()
    hangman = make_hangman(word)
    
    while True: 
        guess = input("Guess a letter: ").lower()
        if hangman(guess):
            print("You guessed the word!")
            break
        
