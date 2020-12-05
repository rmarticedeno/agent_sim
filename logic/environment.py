from random import randint
from utils import Empty, Dirty, Dirty, Corral, Obstacle, generate
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
        return self.generate(Dirty, dirty)

    def geno(self, obstacles):
        return self.generate(Obstacle, obstacles)

    def generate(self, obj, percent):
        count = 0

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i,j] == obj:
                    count += 1

        total = self.rows * self.columns

        actioners = self.childs + [self.robot]

        while ( count / total < percent):
            generate(self.board, actioners, obj)
            count +=1  

    def corrales(self):
        large = max(self.rows, self.columns)

        for i in range(self.n_childs):
            if large == self.rows:
                self.board[i][0] = Corral
            else:
                self.board[0][i] = Corral