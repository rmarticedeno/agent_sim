from utils import get_empty_pos

class Actioner:

    def __init__(self, board):
        self.suffle(board)

    def suffle(self, board):
        self.i, self.j = get_empty_pos(board)

    def action(self, board):
        pass