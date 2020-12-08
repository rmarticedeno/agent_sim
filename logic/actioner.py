from utils import get_empty_pos

class Actioner:

    def __init__(self, i, j):
        self.shuffle(i, j)
        self.type = None

    def shuffle(self, i, j):
        self.i, self.j = i, j

    def action(self, board):
        pass