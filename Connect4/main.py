# TODO: game logic -> gravitation, connection (schau um den marker ob gleiche marker drumrum sind)
# TODO: ai player

import pyautogui
import random
import time
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
winner = Player(markers)


def game():
    global winner
    winner = Player(markers)
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
    allPlacedFields = {}
    for col in range(COLUMNS):
        for row in range(ROWS):
            mk = gameBoard.game_board[row][col]
            if mk != " ":
                allPlacedFields[f"{row}{col}"] = mk
    allConnections = field_connections(allPlacedFields)
    if not is_draw(gameBoard):
        for con in allConnections:
            if len(con) >= 4:
                four_connected(con[0], gameBoard)
    else:
        clear_terminal()
        gameBoard.print()
        print("You drawed!")
        continue_game()


def is_draw(gameBoard):
    for col in range(COLUMNS):
        for row in range(ROWS):
            mk = gameBoard.game_board[row][col]
            if mk == " ":
                return False
    return True


def four_connected(marker, gameBoard):
    clear_terminal()
    global winner
    for player in players:
        if player.marker == marker:
            winner = player
    gameBoard.print()
    print(f"\nYou won {winner.name}!\n"
          f"It only took {21 - winner.pieces} pieces.")
    continue_game()


def continue_game():
    if input("Do you want to play again? (y/n): ") or "y" == "y":
        clear_terminal()
        game()


def field_connections(placed):
    connections = []
    for placedField in placed:
        curr_marker = placed[placedField]
        neighbouring_directions = neighbouring_directions_to_same(placedField, placed, curr_marker)
        for direction in neighbouring_directions:
            connection = [placed[f"{direction[0]}{direction[1]}"]]

            is_second_item = is_second_item_correct(placed, direction, curr_marker)
            if is_second_item:
                connection.append(is_second_item[1])

            is_third_item = is_third_item_correct(placed, direction, curr_marker)
            if is_third_item and is_second_item:
                connection.append(is_third_item[1])

            is_fourth_item = is_fourth_item_correct(placed, direction, curr_marker)
            if is_third_item and is_second_item and is_fourth_item:
                connection.append(is_fourth_item[1])
            connections.append(connection)
    return connections


def is_second_item_correct(placed, direction, curr_marker):
    second_row = direction[0] + direction[2]
    second_col = direction[1] + direction[3]
    if item_check(placed, second_row, second_col, curr_marker):
        return True, curr_marker


def is_third_item_correct(placed, direction, curr_marker):
    third_row = direction[0] + direction[2] + direction[2]
    third_col = direction[1] + direction[3] + direction[3]
    if item_check(placed, third_row, third_col, curr_marker):
        return True, curr_marker


def is_fourth_item_correct(placed, direction, curr_marker):
    fourth_row = direction[0] + direction[2] + direction[2] + direction[2]
    fourth_col = direction[1] + direction[3] + direction[3] + direction[3]
    if item_check(placed, fourth_row, fourth_col, curr_marker):
        return True, curr_marker


def item_check(placed, row, col, marker):
    if f"{row}{col}" in placed:
        if placed[f"{row}{col}"] == marker:
            return True


def neighbouring_directions_to_same(placedField, placed, marker):
    row = int(placedField[:1])
    col = int(placedField[1:])
    directions = []
    for direct in NEIGHBOUR_CONNECTIONS:
        if surrounding_markers(row, col, direct, placed, marker):
            directions.append((row, col, direct[0], direct[1]))
    return directions


def surrounding_markers(row, col, direct, placed, marker):
    new_row = row + direct[0]
    new_col = col + direct[1]
    if 0 <= new_row <= ROWS - 1:
        if 0 <= new_col <= COLUMNS - 1:
            if f"{new_row}{new_col}" in placed:
                if placed[f"{new_row}{new_col}"] == marker:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


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
