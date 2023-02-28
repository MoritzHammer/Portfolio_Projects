import random
# import time


def choose_word():
    with open('GermanWords.txt', 'r', encoding='UTF-8') as f:
        words = f.readlines()
        randomWord = random.choice(words).strip()
        f.close()
    return [randomWord, {char.lower(): False for char in randomWord}]


lives = 6


def start():
    global word
    global guessed
    word = choose_word()
    guessed = []
    show_guessed_progress()
    choose_char()


def choose_char():
    char = input("Please input a character: ").lower()
    if char in word[1] and char not in guessed:
        word[1][char] = True
    else:
        guessed.append(char)
        guessed_chars = ", ".join(c for c in guessed)
        show_hangman_lives()
        print(f"Guessed ({len(guessed)}): {guessed_chars}")

    show_guessed_progress()
    if has_won():
        print("You won")
        print(f"You only guessed wrong {len(guessed)} times.")
        another_game()

    elif not is_dead():
        choose_char()

    else:
        print("You are dead")
        print(f"The word was: '{word[0]}'")
        another_game()


def show_guessed_progress():
    progress = "".join(n if word[1][n.lower()] is True else '_' for n in word[0])
    print(f"({len(word[0])}) {progress}")


def is_dead():
    if len(guessed) >= lives:
        return True
    return False


def has_won():
    for x in word[1]:
        if not word[1][x]:
            return False
    return True


def another_game():
    if input("Do you want to play another game? (y/n): ") == "y":
        start()


def show_hangman_lives():
    if len(guessed) == 0:
        print("  \n" +
              "  \n" +
              "  \n" +
              "  \n" +
              "  \n" +
              "  \n" +
              "  \n")
    elif len(guessed) == 1:
        print("  \n" +
              "  \n" +
              "  \n" +
              "  \n" +
              "  \n" +
              "  ______\n" +
              "  |    |\n")
    elif len(guessed) == 2:
        print("    ||  \n" +
              "    ||  \n" +
              "    ||  \n" +
              "    ||  \n" +
              "    ||  \n" +
              "  __||__\n" +
              "  |    |\n")
    elif len(guessed) == 3:
        print("    ||==========\n" +
              "    ||  \n" +
              "    ||  \n" +
              "    ||  \n" +
              "    ||  \n" +
              "  __||__\n" +
              "  |    |\n")
    elif len(guessed) == 4:
        print("    ||=========*\n" +
              "    ||         |\n" +
              "    ||  \n" +
              "    ||  \n" +
              "    ||  \n" +
              "  __||__\n" +
              "  |    |\n")
    elif len(guessed) == 5:
        print("    ||=========*\n" +
              "    ||         |\n" +
              "    ||         O\n" +
              "    ||  \n" +
              "    ||  \n" +
              "  __||__\n" +
              "  |    |\n")
    elif len(guessed) == 6:
        print("    ||=========*\n" +
              "    ||         |\n" +
              "    ||         O\n" +
              "    ||        /|\\\n" +
              "    ||        / \\\n" +
              "  __||__\n" +
              "  |    |\n")


start()
