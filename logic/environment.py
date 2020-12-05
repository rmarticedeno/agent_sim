
Empty, Dirty, Corral, Obstacle, Chilren, Robot = range(6)


class Environment:

    def __init__(self, rows, columns, n_childs, dirty, t, childs = None, robot = None):
        self.rows = rows
        self.columns = columns
        self.n_childs = n_childs
        self.n_cunas = n_childs
        self.board = [ [Empty] * columns for i in range(rows)]