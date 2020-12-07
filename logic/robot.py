from actioner import Actioner
from utils import Robot_Piece

class Robot(Actioner):

    def __init__(self, i, j):
        super().__init__(i, j)
        self.type = Robot_Piece