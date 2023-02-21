# TODO: board erstellen
# TODO: game logic -> gravitation, connection (schau um den marker ob gleiche marker drumrum sind)
# TODO: arrow über board der zeigt worein
# TODO: ai player

game_board = [6][7]
markers = []
players = []


def set_players():
    player_size = int(input("How much players? (1/2): ") or "2")
    for i in range(player_size):
        player = Player
        players.append(player)


class Board:
    def __init__(self):
        self.filler = " "
        self.innerVerticalBorder = "|"
        self.outerVerticalBorder = "||"
        self.horizontalBorder = "_"


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


