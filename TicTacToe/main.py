from aiplayer import AI
import time
import random

PLAYER_1 = "X"
PLAYER_2 = "O"
p1_name = ""
p2_name = ""
ai = False
columns, rows = 3, 3
WINNING_POSITIONS = [[(0, 0), (0, 1), (0, 2)],  # horizontal
                     [(1, 0), (1, 1), (1, 2)],
                     [(2, 0), (2, 1), (2, 2)],
                     [(0, 0), (1, 0), (2, 0)],  # vertical
                     [(0, 1), (1, 1), (2, 1)],
                     [(0, 2), (1, 2), (2, 2)],
                     [(0, 0), (1, 1), (2, 2)],  # diagonal
                     [(0, 2), (1, 1), (2, 0)]]
field = []
winner = ""


def game_start():
    create_field()
    print_introduction()
    logic()


def create_field():
    global field
    global winner
    field = [["-" for _ in range(columns)] for _ in range(rows)]
    winner = ""


def print_field():
    print("---------------------")
    top_row = "\t  | " + " | ".join(str(x + 1) for x in range(columns))
    print(top_row)
    for n in range(rows):
        row = f"\t{chr(n + 65)} |" + \
               "".join(f" {field[n][m] } |" if m != columns - 1 else f" {field[n][m]}" for m in range(columns))
        print(row)
    print("---------------------")


def print_introduction():
    print("Welcome to tic-tac-toe!"
          "\nYou play by writing the coordinates of the spot you want to mark. "
          "\nFor example: 'A1', 'B2' or 'C1'. ")
    setting()


def setting():
    global p1_name
    global p2_name
    global ai
    players = int(input("Do you want to play alone or with someone else? (1/2): ") or "1")
    p1_name = input("Your name: ") or "Player 1"
    if players == 1:
        ai = True
        global aiPlayer
        aiPlayer = AI()
        aiPlayer.winning_pos = WINNING_POSITIONS
    else:
        p2_name = input("Player 2 name: ") or "Player 2"


def logic():
    play_loop(bool(random.getrandbits(1)))
    if again():
        game_start()


def play_loop(player1):
    print_field()
    mk, co = choose(player1)
    placing_logic(co, mk, player1)
    if winner_logic():
        score()
    else:
        play_loop(not player1)


def choose(player1) -> (str, str):
    global ai
    if player1:
        coordinate = input(f"{p1_name}: ")
        marker = PLAYER_1
    elif not player1 and not ai:
        coordinate = input(f"{p2_name}: ")
        marker = PLAYER_2
    else:
        return ai_choose()
    return marker, coordinate


def ai_choose() -> (str, str):
    print("AI is calculating")
    Start = time.perf_counter()
    aiPlayer.find_and_translate_move(field)
    End = time.perf_counter()
    co = aiPlayer.move
    print(f"It chooses {co} ({End - Start:0.3f} s).")
    return PLAYER_2, co


def placing_logic(co, mk, p1):
    player_column, player_row = int(co[1]) - 1, int(ord(co[0].upper())) - 65
    if player_column >= columns or player_row >= rows:
        print(f"'{co}' is not on the playing field. Please place again. ")
        play_loop(p1)
    spot = field[player_row][player_column]

    if spot != "-":
        print(f"Already placed marker '{spot}' on {co}. Please place again. ")
        play_loop(p1)
    field[player_row][player_column] = mk


def winner_logic() -> bool:
    global winner
    for position in WINNING_POSITIONS:
        p1, p2, p3 = position[0], position[1], position[2]
        if field[p1[0]][p1[1]] == field[p2[0]][p2[1]] and field[p2[0]][p2[1]] == field[p3[0]][p3[1]]:
            if field[p1[0]][p1[1]] != "-":
                if field[p1[0]][p1[1]] == PLAYER_1:
                    winner = PLAYER_1
                else:
                    winner = PLAYER_2

    if not any((field[row][col] == "-" for row in range(rows) for col in range(columns))):
        draw_score()

    if winner != "":
        return True


def draw_score():
    print("You have drawn.")
    print_field()
    if again():
        game_start()
    else:
        exit()


def score():
    if winner == PLAYER_1:
        print(f"Congratulations {p1_name}! ")
    elif winner == PLAYER_2:
        if not ai:
            print("You won.")
            print_field()
            print(f"Good Job {p2_name} :)")
        else:
            print_field()
            print(f"And wins.")


def again():
    if input("Do you want to play again? (y/n): ") != "n":
        return True
    return False


game_start()
