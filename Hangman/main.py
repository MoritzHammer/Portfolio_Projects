import random
import requests

lives = 6
word_and_slice = []
guessed = []


def start():
    global word_and_slice
    global guessed
    word_and_slice = choose_word_and_slice()
    guessed = []
    show_guessed_progress()
    choose_char()


def choose_word_and_slice():
    with open('GermanWords.txt', 'r', encoding='UTF-8') as f:
        words = f.readlines()
        randomWord = random.choice(words).strip()
        f.close()
    return [randomWord, {char.lower(): False for char in randomWord}]


def choose_char():
    char = input("Please input a character: ").lower()
    process_input(char)


def process_input(char):
    if char.lower() == "joker" and not has_won() and not is_dead():
        print(f"A character in the word is: {joker_char(0)}")
    elif char in word_and_slice[1] and char not in guessed:
        word_and_slice[1][char] = True
    else:
        guessed.append(char)
        guessed_chars = ", ".join(c for c in guessed)
        show_hangman_lives()
        print(f"Guessed ({len(guessed)}): {guessed_chars}")
    game_logic()


def game_logic():
    show_guessed_progress()
    if has_won():
        scoreboard(True)
        another_game()
    elif not is_dead():
        choose_char()
    else:
        scoreboard(False)
        another_game()


def scoreboard(win):
    fr = frequency()
    if win:
        print("You won")
        print(f"You only guessed wrong {len(guessed)} times.")
    else:
        print("You are dead")
        print(f"The word was: '{word_and_slice[0]}'")
    print(f"The word '{word_and_slice[0]}' appears in the internet a total of "
          f"{format(fr[0], ',d').replace(',','.')} times of {format(fr[1], ',d').replace(',','.')} entries."
          f"\nThat is {fr[0]/fr[1]} %")


def joker_char(i):
    c = word_and_slice[0][i]
    if word_and_slice[1][c.lower()] is True:
        return joker_char(i + 1)
    return c


def show_guessed_progress():
    progress = "".join(n if word_and_slice[1][n.lower()] is True else '_' for n in word_and_slice[0])
    print(f"({len(word_and_slice[0])}) {progress}")


def is_dead():
    if len(guessed) >= lives:
        return True
    return False


def has_won():
    for x in word_and_slice[1]:
        if not word_and_slice[1][x]:
            return False
    return True


def frequency():
    url = f"https://www.dwds.de/api/frequency/?q={word_and_slice[0]}"
    response = requests.get(url=url).json()
    return int(response["hits"]), int(response["total"])


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
