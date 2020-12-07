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
            self.robot = None
            self.childs = []
            
            for _ in range(self.n_childs):
                i, j = self.get_empty_pos()
                self.childs.append(Child(i, j))

            i, j = self.get_empty_pos()
            self.robot = Robot(i, j)
            
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
        actioners = []

        if self.childs and len(self.childs):
            actioners += self.childs
        if self.robot:
            actioners += [self.robot]

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


