from actioner import Actioner
from utils import Children

class Child(Actioner):

    def __init__(self, i, j):
        super().__init__(i, j)
        self.type = Children