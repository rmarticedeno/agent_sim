from random import randint


Empty, Dirty, Corral, Obstacle, Chilren, Robot = range(6)


class Environment:

    def __init__(self, rows, columns, n_childs, dirty, obstacles, t, childs = None, robot = None):
        self.rows = rows
        self.columns = columns
        self.n_childs = n_childs
        self.n_cunas = n_childs
        self.board = [ [Empty] * columns for i in range(rows)]
        self.t = t
        self.moment = 0

        if not childs:
            #self.childs = [ Child ] * self.n_childs 
            #self.robot = Robot()
            pass
            
        else:
            self.childs = childs
            self.robot = robot

            for i in range(len(self.childs)):
                #self.childs[i].shuffle()
                pass
            #self.robot.shuffle()
            

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

        while ( count / total < percent):
            i = randint(0, self.rows-1)
            j = randint(0, self.columns-1)

            if self.board[i][j] == Empty:
                self.board[i][j] = obj
                count +=1  