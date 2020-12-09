from random import randint, choice
from .utils import Empty, Dirty, Corral, Obstacle, Children, Robot_Piece
from .utils import Up, Down, Left, Right, Stay, dx, dy, dx_complete, dy_complete
from .child import Child
from .robot import Robot




class Environment:

    def __init__(self, rows, columns, n_childs, dirty, obstacles, t, childs = None, robot = None, strategy_one = False):
        self.rows = rows
        self.columns = columns
        self.n_childs = n_childs
        self.n_cunas = n_childs
        self.init_dirty = dirty
        self.init_obst = obstacles
        self.t = t
        self.strategy_one = strategy_one

    def reset(self, dirty, obstacles, childs = None, robot = None, complete=False):
        if complete:
            self.moment = 0
            self.tie = False
            self.lost = False
            self.win = False
            self.ended = False
            self.dirty = 0

        self.board = [ [Empty] * self.columns for i in range(self.rows)]

        self.corrales()

        if not childs:
            self.robot = None
            self.childs = []
            
            for k in range(self.n_childs):
                i, j = self.get_empty_pos()
                self.childs.append(Child(i, j))

            i, j = self.get_empty_pos()
            self.robot = Robot(i, j, self.strategy_one)
            
        else:
            self.childs = childs
            self.robot = robot

            for i in range(len(self.childs)):
                k,j = self.get_empty_pos()
                self.childs[i].shuffle(k, j)

            i,j = self.get_empty_pos()
            self.robot.shuffle(i, j)
            

        self.gend(dirty)

        self.geno(obstacles)

    def simulate(self):
        self.reset(self.init_dirty, self.init_obst, complete=True)

        while (self.moment < 100*self.t):
            
            dirty = self.object_percent(Dirty)

            self.dirty += dirty

            if dirty >= 0.6:    
                self.lost = True
                break
            
            for child in self.childs:
                if not child.is_in_corral:
                    break
            else:
                dirty = False
                for i in range(self.rows):
                    for j in range(self.columns):
                        if self.board[i][j] == Dirty:
                            dirty = True
                            break
                    if dirty:
                        break
                else:
                    self.win = True
                    break
            
            move = self.robot.action(self)

            self.make_robot_move(move)

            for i in range(self.n_childs):
                boy = self.childs[i]
                if not boy.is_charged and not boy.is_in_corral:
                    move = boy.action(self)
                    self.make_child_move(i, move)

            if self.moment > 0 and self.moment % self.t == 0:
                dirty = self.object_percent(Dirty)
                obstacles = self.object_percent(Obstacle)
                self.reset(dirty, obstacles, self.childs, self.robot)

            # print(self)
            # input()

            self.moment += 1

        self.ended = True
        self.tie = not self.win and not self.lost

    def make_robot_move(self, move):
        if move != Stay:

            x = self.robot.i + dx[move]
            y = self.robot.j + dy[move]

            piece = self.board[x][y] if self.board[x][y] == Corral else self.get_piece(x,y)

            if piece == Corral:
                for k in range(self.n_childs):
                    if self.childs[k].is_charged:
                        self.childs[k].is_charged = False
                        self.childs[k].is_in_corral = True
                        self.childs[k].i = x
                        self.childs[k].j = y
                        self.robot.charge_child = False

            elif piece == Children:
                for k in range(self.n_childs):
                    if self.childs[k].i == x and self.childs[k].j == y:
                        self.childs[k].is_charged = True
                        self.robot.charge_child = True
                        self.childs[k].i = -1
                        self.childs[k].j = -1

            elif piece == Dirty:
                self.board[x][y] = Empty

            self.robot.i = x
            self.robot.j = y

    def make_child_move(self, i , move):
        x, y = self.childs[i].i, self.childs[i].j

        if self.possible_child_move(x, y, move):
            x_n = x + dx[move]
            y_n = y + dy[move]

            self.childs[i].i = x_n
            self.childs[i].j = y_n

            if self.board[x_n][y_n] == Obstacle:
                x_o, y_o = self.find_last_empty(x, y, move)
                self.board[x_o][y_o] = Obstacle
                self.board[x_n][y_n] = Empty

        self.child_mess(x, y)


    def object_percent(self, obt):
        count = 0

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == obt:
                    count += 1
        
        total = self.rows * self.columns

        return count / total

    def gend(self, dirty):
        return self.generate_object(Dirty, dirty)

    def geno(self, obstacles):
        return self.generate_object(Obstacle, obstacles)

    def generate_object(self, obj, percent):
        count = 0

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == obj:
                    count += 1

        total = self.rows * self.columns

        while ( count / total < percent):
            self.generate(obj)
            count +=1  

    def corrales(self):
        large = max(self.rows, self.columns)

        for i in range(self.n_childs):
            if large == self.rows:
                self.board[i][0] = Corral
            else:
                self.board[0][i] = Corral


    def get_empty_pos(self):
        board = self.board
        actioners = self.get_actioners()

        others = [(x.i,x.j) for x in actioners] 

        max_row = self.rows - 1
        max_column = self.columns - 1

        i = 0
        j = 0

        while(True):
            i = randint(0, max_row)
            j = randint(0, max_column)

            if board[i][j] == Empty and (i,j) not in others:
                break

        return i,j

    def generate(self, obj):
        i,j = self.get_empty_pos()
        self.board[i][j] = obj

    def valid_position(self, x, y):
        return x >= 0 and y >= 0 and x < self.rows - 1 and y < self.columns

    def get_actioners(self):

        actioners = []

        if self.childs and len(self.childs):
            actioners += self.childs
        if self.robot:
            actioners += [self.robot]
        
        return actioners

    def get_piece(self, x, y):
        actioners = self.get_actioners()

        for act in actioners:
            if act.i == x and act.j == y:
                return act.type
        
        return self.board[x][y]

    def __str__(self):
        ans = ""
        for i in range(self.rows):
            for j in range(self.columns):
                pos = ""
                for act in self.childs:
                    if act.i == i and act.j == j:
                        pos += " B "

                if self.robot.i == i and self.robot.j == j:
                    pos += " R "
                
                piece = self.board[i][j]

                if len(pos) > 3:
                    print(f"Error at {i},{j} {pos}")
                    
                elif len(pos) == 3:
                    ans += pos
                    continue                

                if piece == Empty:
                    pos += " - "
                elif piece == Dirty:
                    pos += " D "
                elif piece == Corral:
                    pos += " C "
                elif piece == Obstacle:
                    pos += " O "
                
                ans += pos
            ans += "\n"
        return ans

    def __repr__(self):
        return str(self)

    def get_surround_positions(self, x, y): 
        acc = []

        for i in range(8):
            x_n = x + dx_complete[i]
            y_n = y + dy_complete[i]
            if self.valid_position(x_n , y_n):
                acc.append((x_n, y_n))

        return acc

    def get_surround_object(self, x, y, obj):
        pos = self.get_surround_positions(x, y)
        result = []
        
        for (x,y) in pos:
            if obj <= 4:
                if self.board[x][y] == obj:
                    result.append((x,y))

            elif obj == Children:
                for child in self.childs:
                    if child.x == x and child.y == y:
                        result.append((x,y))

            else:
                if self.robot.x == x and self.robot.y == y:
                    result.append((x,y))

        return result
        
    def is_empty(self, x, y):
        for actioner in self.get_actioners():
            if actioner.i == x and actioner.j == y:
                return False
        return self.valid_position(x,y) and self.board[x][y] == Empty

    def possible_child_move(self, x, y , move):
        x_n = x + dx[move]
        y_n = y + dy[move]

        if self.valid_position(x_n,y_n) and self.board[x_n][y_n] == Obstacle:
            return self.possible_child_move(x_n, y_n, move)

        if not self.is_empty(x_n, y_n):
            return False
        
        return True
            
    def find_last_empty(self, x, y, move):
        x_n = x + dx[move]
        y_n = y + dy[move]

        if self.is_empty(x_n, y_n):
            return (x_n, y_n)

        return self.find_last_empty(x_n, y_n, move)

    def child_mess(self, x, y):
        childs = len(self.get_surround_object(x,y, Children))

        garbage = 1
        if childs == 2:
            garbage = 3
        elif childs >= 3:
            garbage = 6

        surround = self.get_surround_object(x, y, Empty) + [(x,y)]

        while True:
            if not len(surround) or not garbage:
                break

            x, y = choice(surround)

            self.board[x][y] = Dirty

            surround.remove((x,y))

            garbage -= 1

    def find_nearest_object_by_func(self, x, y, func, message = "mensaje"):
        distance = [[-1] * self.columns for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                distance[i][j] = abs(i - x) + abs(j - y)

        _min = self.rows * self.columns

        for i in range(self.rows):
            for j in range(self.columns):
                dist = distance[i][j]
                # if func(i, j, self):
                #     print("paso ", self.board[i][j], distance[i][j])
                if func(i, j, self) and (dist > 0 or (dist >=0 and self.board[x][y] == Corral)) and dist < _min:
                    _min = dist

        for i in range(self.rows):
            for j in range(self.columns):
                if distance[i][j] == _min and func(i,j,self):
                    #print(i,j, distance[i][j])
                    return (i, j, distance[i][j])

        # for child in self.childs:
        #     print(child.is_in_corral)
        #     print(child.i, child.j)
        #     print("charded child", child.is_charged)

        # print(self)
        # print(func(x,y,self) == Children)
        # print(_min)
        # print(message)

        # print("state")
        # print(self.board[0][0])
        # print(self.board[1][0])
        # print(self.board[2][0])
        # print(self.get_piece(0,0))
        # print(self.get_piece(1,0))
        # print(self.get_piece(2,0))

        # return -1, -1, -1
        
    def no_free_child(self):
        for child in self.childs:
            if not child.is_in_corral:
                return False
        return True