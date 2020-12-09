from .actioner import Actioner
from .utils import Children, Up, Down, Left, Right, Stay
from random import randint

class Child(Actioner):

    def __init__(self, i, j):
        self.is_in_corral = False
        super().__init__(i, j)
        self.type = Children
        self.is_charged = False

    def action(self, env):
        actions = [Up, Down, Left, Right, Stay]
        index = randint(0,4)
        return actions[index]

    def shuffle(self, i, j):
        if not self.is_in_corral:
            self.i, self.j = i, j