from utils import get_empty_pos

class Actioner:

    def __init__(self, board, actioners):
        self.suffle(board, actioners)

    def suffle(self, board, actioners):
        self.i, self.j = get_empty_pos(board, actioners)

    def action(self, board):
        pass