# TODO: game logic -> gravitation, connection (schau um den marker ob gleiche marker drumrum sind)
# TODO: ai player
import time

import pyautogui
import random
from pynput import keyboard

from player import Player

markers = []
players = []
ARROW_POSITIONS = ["\t    ", "\t        ", "\t            ", "\t                ",
                   "\t                    ", "\t                        ", "\t                            "]
NEIGHBOUR_CONNECTIONS = [(1, -1), (1, 0), (1, 1),
                         (0, -1),         (0, 1),
                         (-1, -1), (-1, 0), (-1, 1)]
ROWS = 6
COLUMNS = 7


class Board:
    def __init__(self):
        self.innerVerticalBorder = " | "
        self.outerVerticalBorder = "||"
        self.horizontalBorder = "_______________________________"
        self.game_board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

    def print(self):
        print("\t _______________________________")
        for i in range(ROWS):
            row = f"\t || "
            for j in range(COLUMNS):
                if j != COLUMNS - 1:
                    row += f"{self.game_board[i][j]} | "
                else:
                    row += self.game_board[i][j]
            row += f" ||"
            print(row)
        print("\t -------------------------------\n"
              "\t ||                           ||\n"
              "\t//\\\\                         //\\\\")


def set_players():
    player_size = int(input("How much players? (1/2): ") or "2")
    for i in range(player_size):
        global markers
        player = Player(markers)
        player.set_name(i)
        markers = player.get_taken_markers()
        players.append(player)


now_playing_player = Player(markers)


def game():
    i = 0
    press = True
    gameBoard = Board()
    start_up(gameBoard)

    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.esc:
                break
            elif event.key == keyboard.Key.left:
                i -= 0.5
                if i < 0:
                    i = 6.5
                new_cycle(gameBoard, i)
            elif event.key == keyboard.Key.right:
                i += 0.5
                if i > 6:
                    i = -0.5
                new_cycle(gameBoard, i)
            elif event.key == keyboard.Key.space:
                gameBoard = drop_piece(gameBoard, i, press)
                press = not press
                i = 0
                new_cycle(gameBoard, i)


def start_up(gameBoard):
    global now_playing_player
    set_players()
    clear_terminal()

    player_sequence()
    now_playing_player = players[0]
    new_cycle(gameBoard, 0)


def drop_piece(gameBoard, i, keyboardinputIsPressed):
    j = ROWS - 1
    new_board = gameBoard
    if keyboardinputIsPressed:
        for _ in range(ROWS):
            if gameBoard.game_board[j][int(i)] == " ":
                gameBoard.game_board[j][int(i)] = now_playing_player.marker
                player_switch()
                return gameBoard
            elif j >= 0:
                j -= 1
            else:
                print("Column already full. Choose again")
                new_cycle(gameBoard, i)
    return new_board


def game_logic(gameBoard):
    allConnections = []
    allPlacedFields = {}
    for col in range(COLUMNS):
        for row in range(ROWS):
            mk = gameBoard.game_board[row][col]
            if mk != " ":
                allPlacedFields[f"{row}{col}"] = mk
    print(allPlacedFields)
    allConnections = field_connections(allPlacedFields)
    print(allConnections)
    for con in allConnections:
        if len(con) >= 4:
            print(f"Winner {now_playing_player.marker}")


def field_connections(placed):
    connections = []
    for placedField in placed:
        connection = []
        print(f"{placedField}--------------")
        print(placed[placedField])
        directions = neighbour_connections(placedField, placed, placed[placedField])
        for direction in directions:
            connection.append(placed[direction[0]][direction[1]])
            connection.append(placed[direction[0] + direction[2]][direction[1] + direction[3]])
            try:
                connection.append(placed[direction[0] + direction[2] + direction[2]]
                                        [direction[1] + direction[3] + direction[3]])
                try:
                    connection.append(placed[direction[0] + direction[2] + direction[2] + direction[2]]
                                            [direction[1] + direction[3] + direction[3] + direction[3]])
                finally:
                    continue
            finally:
                continue
        connections.append(connection)
    return connections


def neighbour_connections(placedField, placed, marker):
    row = int(placedField[:1])
    col = int(placedField[1:])
    directions = []
    for direct in NEIGHBOUR_CONNECTIONS:
        new_row = row + direct[0]
        new_col = col + direct[1]
        try:
            print(new_row,  new_col, placed[new_row][new_col])
            if placed[new_row][new_col] == marker:
                directions.append((row, col, direct[0], direct[1]))
        finally:
            print("fin")
            continue
    return directions


def player_switch():
    global now_playing_player
    n = now_playing_player.name
    for player in players:
        if player.name == n:
            player.pieces -= 1
        else:
            now_playing_player = player


def player_sequence():
    global players
    new_sequence = [which_player_starts()]
    for player in players:
        if player != new_sequence[0]:
            new_sequence.append(player)
    players = new_sequence


def which_player_starts():
    return random.choice(players)


def new_cycle(gameBoard, i):
    clear_terminal()
    game_logic(gameBoard)
    print_players()
    print_player_turn()
    print_arrow(i)
    gameBoard.print()


def print_players():
    if len(players) > 1:
        for player in players:
            player.print_me()
    else:
        players[0].print_me()
        # TODO: AI print


def print_player_turn():
    print(f"{now_playing_player.name} turns now.")


def print_arrow(i):
    arrow = f"\n{ARROW_POSITIONS[int(i)]}{now_playing_player.marker}\n" \
            f"{ARROW_POSITIONS[int(i)]}|\n" \
            f"{ARROW_POSITIONS[int(i)]}V"
    print(arrow)


def clear_terminal():
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'z')

game()
