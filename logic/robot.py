from actioner import Actioner
from utils import Empty, Dirty, Corral, Obstacle, Children, Robot_Piece, dx, dy, Up, Down, Left, Right, Stay 
from random import choice

class Robot(Actioner):

    def __init__(self, i, j):
        super().__init__(i, j)
        self.type = Robot_Piece
        self.charge_child = False

    def action(self, board):
        actions = [ Up, Down, Left, Right ]
        results = []

        for act in actions:
            if self.valid_robot_move(act, board):
                results.append(act)
        
        if len(results):
            return choice(results)

        return Stay
    
    def valid_robot_move(self, move, env):
        x = self.i + dx[move]
        y = self.j + dy[move]

        if not env.valid_position(x,y):
            return False
        
        piece = env.board[x][y]

        if piece == Obstacle:
            return False
        
        if piece == Corral and not self.charge_child:
            return False

        if piece == Children and self.charge_child:
            return False
        
        return True