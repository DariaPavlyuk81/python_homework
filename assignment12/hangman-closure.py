#Task4
# hangman-closure.py

def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())
        displayed = "".join([char if char in guesses else "_" for char in secret_word])
        print("Current word:", displayed)
        return set(secret_word).issubset(set(guesses))

    return hangman_closure



def main():
    secret_word = input("Enter the secret word: ").lower()
    print("\n" * 50)  # Clear screen

    guess_letter = make_hangman(secret_word)

    while True:
        letter = input("Guess a letter: ").lower()
        if len(letter) != 1 or not letter.isalpha():
            print("Please enter a single alphabetical character.")
            continue

        done = guess_letter(letter)
        if done:
            print("Congratulations! You guessed the word:", secret_word)
            break

if __name__ == "__main__":
    main()
