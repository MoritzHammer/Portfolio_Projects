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
    top_row = "  | "
    top_row += " | ".join(str(x + 1) for x in range(columns))
    print(f"\t{top_row}")
    for n in range(rows):
        char = chr(n + 65)
        row = f"{char} |"
        for m in range(columns):
            row += f" {field[n][m]}"
            if m != columns - 1:
                row += f" |"
        print(f"\t{row}")
    print("---------------------")


def print_introduction():
    print("Welcome to tic-tac-toe!")
    print("You play by writing the coordinates of the spot you want to mark. "
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
    aiPlayer.start_move(field)
    End = time.perf_counter()
    co = aiPlayer.move
    print(f"It chooses {co} ({End - Start:0.3f} s).")
    return PLAYER_2, co


def placing_logic(co, mk, p1):
    spot = "-"
    player_column = int(co[1]) - 1
    player_row = int(ord(co[0].upper())) - 65
    if player_column >= columns or player_row >= rows:
        print(f"'{co}' is not on the playing field. Please place again. ")
        play_loop(p1)
    else:
        spot = field[player_row][player_column]

    if spot != "-":
        print(f"Already placed marker '{spot}' on {co}. Please place again. ")
        play_loop(p1)
    else:
        field[player_row][player_column] = mk


def winner_logic() -> bool:
    global winner
    for position in WINNING_POSITIONS:
        p1 = position[0]
        p2 = position[1]
        p3 = position[2]
        if field[p1[0]][p1[1]] == field[p2[0]][p2[1]] and field[p2[0]][p2[1]] == field[p3[0]][p3[1]]:
            if field[p1[0]][p1[1]] != "-":
                if field[p1[0]][p1[1]] == PLAYER_1:
                    winner = PLAYER_1
                else:
                    winner = PLAYER_2
    draw = True
    for col in range(columns):
        for row in range(rows):
            if field[row][col] == "-":
                draw = False
    if draw:
        draw_score()

    if winner != "":
        return True


def draw_score():
    print("You have drawn.")
    print_field()
    if again():
        game_start()

def score():
    if not ai:
        print("You won.")
        print_field()
        if winner == PLAYER_1:
            print(f"Congratulations {p1_name}! ")
        elif winner == PLAYER_2:
            print(f"Good Job {p2_name} :)")
    else:
        if winner == PLAYER_1:
            print(f"Congratulations {p1_name}! \n You won.")
        elif winner == PLAYER_2:
            print_field()
            print(f"And wins.")


def again():
    repeat = input("Do you want to play again? (y/n): ")
    if repeat != "n":
        return True
    return False

game_start()
