from .actioner import Actioner
from .utils import Empty, Dirty, Corral, Obstacle, Children, Robot_Piece, dx, dy, Up, Down, Left, Right, Stay 
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

        if self.charge_child:
            for res in results:
                if board.board[self.i + dx[res]][self.j + dy[res]] == Corral:
                    return res

        
        if len(results):
            if self.charge_child:
                return self.get_next_emtpy_corral(results, board)

            if self.strategy_one:
                return self.strategy_one(results, board)
            else:
                return self.strategy_two(results, board)

        return Stay
    
    def valid_robot_move(self, move, env): 
        x = self.i + dx[move]
        y = self.j + dy[move]

        if not env.valid_position(x,y):
            return False
        
        piece = env.board[x][y]

        if piece == Corral and not self.charge_child:
            return False

        piece = env.get_piece(x,y)

        if piece == Obstacle:
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

    def strategy_two(self, results, env):
        if env.object_percent(Dirty) >= 0.4 or env.no_free_child():
            return self.get_next_by_func(results, env, lambda x,y,env: env.board[x][y] == Dirty)
        else:
            return self.get_next_by_func(results, env, lambda x,y,env: env.get_piece(x,y) == Children, "children")

    def get_next_emtpy_corral(self, results, env):
        return self.get_next_by_func(results, env, valid_corral, "corral")

    def get_next_by_func(self, results, env, func, mensage = "message"):

        #print("charged", self.charge_child)
        
        x,y,value = env.find_nearest_object_by_func(self.i, self.j, func, mensage)

        # if x == -1:
        #     print(mensage)
        #     return Stay

        dist = []

        for res in results:
            dist.append(manhattan_distance(x,y, self.i + dx[res], self.j + dy[res]))

        _min = min(dist)

        finals = []

        for res in results:
            if manhattan_distance(x,y, self.i + dx[res], self.j + dy[res]) == _min:
                finals.append(res)

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