from random import randint
from utils import Empty, Dirty, Dirty, Corral, Obstacle
from utils import Up, Down, Left, Right, Stay, dx, dy
from child import Child
from robot import Robot




class Environment:

    def __init__(self, rows, columns, n_childs, dirty, obstacles, t, childs = None, robot = None):
        self.rows = rows
        self.columns = columns
        self.n_childs = n_childs
        self.n_cunas = n_childs
        self.board = [ [Empty] * columns for i in range(rows)]
        self.t = t
        self.moment = 0

        self.corrales()

        if not childs:
            self.childs = []
            
            for _ in range(self.n_childs):
                self.childs.append(Child(self.board, self.childs))
            self.robot = Robot(self.board, self.childs)
            
        else:
            self.childs = childs
            self.robot = robot

            for i in range(len(self.childs)):
                actioners = self.childs
                self.childs[i].shuffle(self.board, actioners)
            self.robot.shuffle(self.board, self.childs)
            

        self.gend(dirty)

        self.geno(obstacles)

    def gend(self, dirty):
        return self.generate_object(Dirty, dirty)

    def geno(self, obstacles):
        return self.generate_object(Obstacle, obstacles)

    def generate_object(self, obj, percent):
        count = 0

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i,j] == obj:
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
        actioners = self.childs + [self.robot]
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
    
    def __str__(self):
        ans = ""
        for i in range(self.rows):
            for j in range(self.columns):
                pos = ""
                for act in self.childs:
                    if act.x == i and act.y == j:
                        pos += " B "

                if self.robot.x == i and self.robot.y == i:
                    pos += " R "
                
                piece = self.board[i][j]

                if piece == Empty:
                    pos += " - "
                elif piece == Dirty:
                    pos += " D "
                elif piece == Corral:
                    pos += " C "
                elif piece == Obstacle:
                    pos += " O "

                if len(pos) > 3:
                    print(f"Error at {i},{j} {pos}")
                
                ans += pos
            ans += "\n"

    def __repr__(self):
        return str(self)


