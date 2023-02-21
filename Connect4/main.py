# TODO: board erstellen
# TODO: game logic -> gravitation, connection (schau um den marker ob gleiche marker drumrum sind)
# TODO: arrow über board der zeigt worein
# TODO: ai player

import pyautogui
from pynput import keyboard

markers = []
players = []
ARROW_POSITIONS = ["\t    ", "\t        ", "\t            ", "\t                ",
                   "\t                    ", "\t                        ", "\t                            "]
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


class Player:
    def __init__(self, marker_set):
        self.name = self.set_name()
        self.marker = self.set_marker()
        self.taken_markers = marker_set

    @staticmethod
    def set_name() -> str:
        return input("What is your name?: ")

    def set_marker(self) -> chr:
        for c in self.name:
            if c not in self.taken_markers:
                self.taken_markers.append(c)
                return c

    def get_taken_markers(self) -> str:
        if self.marker is not None:
            return self.taken_markers


def set_players():
    player_size = int(input("How much players? (1/2): ") or "2")
    for i in range(player_size):
        player = Player
        players.append(player)


def game():
    i = 2
    gameBoard = Board()
    print_arrow(i)
    gameBoard.print()

    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.esc:
                break
            elif event.key == keyboard.Key.left:
                i -= 1
                if i < 0:
                    i = 14
                clear_terminal()
                print_arrow(i)
                gameBoard.print()
            elif event.key == keyboard.Key.right:
                i += 1
                if i > 14:
                    i = 0
                clear_terminal()
                print_arrow(i)
                gameBoard.print()


def print_arrow(i):
    arrow = f"{ARROW_POSITIONS[int(i/2)-1]}|\n" \
            f"{ARROW_POSITIONS[int(i/2)-1]}V"
    print(arrow)


def clear_terminal():
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'z')


game()
