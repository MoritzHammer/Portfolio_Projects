from math import inf


class AI:
    def __init__(self):
        self.state = []
        self.move = ""

    def find_move(self, state, player):
        winner_loser, done = self.check(state)
        if done == "Done" and winner_loser == 'O':
            return 1, 0
        elif done == "Done" and winner_loser == 'X':
            return -1, 0
        elif done == "Draw":
            return 0, 0

        moves = []
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    empty_cells.append(i * 3 + (j + 1))

        for empty_cell in empty_cells:
            move = {}
            move['index'] = empty_cell
            new_state = self.copy_game_state(state)
            self.play_move(new_state, player, empty_cell)

            if player == 'O':  # If AI
                result, _ = self.find_move(new_state, 'X')
                move['score'] = result
            else:
                result, _ = self.find_move(new_state, 'O')
                move['score'] = result
            moves.append(move)

        # Find best move
        best_move = None
        if player == 'O':
            best = -inf
            for move in moves:
                if move['score'] > best:
                    best = move['score']
                    best_move = move['index']
        else:
            best = inf
            for move in moves:
                if move['score'] < best:
                    best = move['score']
                    best_move = move['index']

        return best, best_move

    def check(self, game_state):

        #  horizontals
        if game_state[0][0] == game_state[0][1] and game_state[0][1] == game_state[0][2] and game_state[0][0] != ' ':
            return game_state[0][0], "Done"
        if game_state[1][0] == game_state[1][1] and game_state[1][1] == game_state[1][2] and game_state[1][0] != ' ':
            return game_state[1][0], "Done"
        if game_state[2][0] == game_state[2][1] and game_state[2][1] == game_state[2][2] and game_state[2][0] != ' ':
            return game_state[2][0], "Done"

        #  verticals
        if game_state[0][0] == game_state[1][0] and game_state[1][0] == game_state[2][0] and game_state[0][0] != ' ':
            return game_state[0][0], "Done"
        if game_state[0][1] == game_state[1][1] and game_state[1][1] == game_state[2][1] and game_state[0][1] != ' ':
            return game_state[0][1], "Done"
        if game_state[0][2] == game_state[1][2] and game_state[1][2] == game_state[2][2] and game_state[0][2] != ' ':
            return game_state[0][2], "Done"

        #  diagonals
        if game_state[0][0] == game_state[1][1] and game_state[1][1] == game_state[2][2] and game_state[0][0] != ' ':
            return game_state[1][1], "Done"
        if game_state[2][0] == game_state[1][1] and game_state[1][1] == game_state[0][2] and game_state[2][0] != ' ':
            return game_state[1][1], "Done"

        draw_flag = 0
        for i in range(3):
            for j in range(3):
                if game_state[i][j] == ' ':
                    draw_flag = 1
        if draw_flag == 0:
            return None, "Draw"
        return None, "Not Done"

    def play_move(self, state, player, block_num):
        if state[int((block_num - 1) / 3)][(block_num - 1) % 3] == ' ':
            state[int((block_num - 1) / 3)][(block_num - 1) % 3] = player

    def copy_game_state(self, state):
        new_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        for i in range(3):
            for j in range(3):
                new_state[i][j] = state[i][j]
        return new_state

    def find_and_translate_move(self, field):
        state = [[y.replace("-", " ") for y in x] for x in field]
        _, block_choice = self.find_move(state, "O")
        self.move = f"{chr(int((block_choice - 1) / 3) + 65)}{(block_choice - 1) % 3 + 1}"
