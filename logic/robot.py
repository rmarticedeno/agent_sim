from actioner import Actioner
from utils import Empty, Dirty, Corral, Obstacle, Children, Robot_Piece, dx, dy, Up, Down, Left, Right, Stay 
from random import choice

class Robot(Actioner):

    def __init__(self, i, j, strategy1 = True):
        super().__init__(i, j)
        self.type = Robot_Piece
        self.charge_child = False
        self.strategy1 = strategy1

    def action(self, board):
        actions = [ Up, Down, Left, Right ]
        results = []

        for act in actions:
            if self.valid_robot_move(act, board):
                results.append(act)
        
        if len(results):
            print("charged", self.charge_child)
            if self.charge_child:
                return self.get_next_emtpy_corral(results, board)

            if self.strategy_one:
                return self.strategy_one(results, board)

        return Stay
    
    def valid_robot_move(self, move, env): 
        x = self.i + dx[move]
        y = self.j + dy[move]

        if not env.valid_position(x,y):
            return False
        
        piece = env.get_piece(x,y)

        if piece == Obstacle:
            return False
        
        if piece == Corral and not self.charge_child:
            return False

        if piece == Children and self.charge_child:
            return False
        
        return True
    
    def calc_score(self, move, env):
        x = self.i + dx[move]
        y = self.j + dy[move]

        score = 0

        if env.board[x][y] == Dirty:
            score = 1

            others = env.get_surround_object(x,y, Dirty)

            score += len(others)

        elif env.board[x][y] == Children:
            if not self.charge_child:
                score += 11
        
        elif env.board[x][y] == Corral:
            if self.charge_child:
                score += 11

        return score

    def strategy_one(self, results, env):
        _max = max([self.calc_score(x, env) for x in results])

        choices = []
        
        for x in results:
            if self.calc_score(x, env) == _max:
                choices.append(x)
        
        if len(choices):
            return choice(choices)

        return Stay

    def get_next_emtpy_corral(self, results, env):
        
        x,y,distance = env.find_nearest_object_by_func(self.i, self.j, valid_corral)

        dist = []

        for res in results:
            dist.append(manhattan_distance(x,y, self.i + dx[res], self.j + dy[res]))

        _min = min(dist)

        finals = []

        for res in results:
            if manhattan_distance(x,y, self.i + dx[res], self.j + dy[res]) == _min:
                finals.append(res)

        print(distance)

        return choice(finals)


def valid_corral(x, y, env):
    if env.board[x][y] != Corral:
        return False
    
    for child in env.childs:
        if child.i == x and child.j == y:
            return False
    
    return True

def manhattan_distance(x,y ,i,j):
    return abs(x - i) + abs(y - j)