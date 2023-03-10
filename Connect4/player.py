
class Player:
    def __init__(self, marker_set):
        self.name = ""
        self.taken_markers = marker_set
        self.marker = ""
        self.piece_size = 21

    def set_name(self, i):
        self.name = input("What is your name?: ") or f"Player{i + 1}"
        self.marker = self.set_marker()

    def set_marker(self) -> chr:
        for c in self.name:
            if c not in self.taken_markers:
                self.taken_markers.append(c)
                return c

    def get_taken_markers(self) -> str:
        if self.marker is not None:
            return self.taken_markers

    def print_me(self):
        pieces = "".join(self.marker for _ in range(self.piece_size))
        print(f"{self.name}'s Markers({self.piece_size})\t {pieces}")
