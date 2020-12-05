
from random import randint

Empty, Dirty, Corral, Obstacle, Chilren, Robot = range(6)

Up, Down, Left, Right, Stay = range(5)

dx = [0, 0, -1, 1]
dy = [1, -1, 0, 0]

def generate(board, obj):
    max_row = len(board) - 1
    max_column = len(board[0]) - 1

    while(True):
        i = randint(0, max_row)
        j = randint(0, max_column)

        if board[i][j] == Empty:
            board[i][j] = obj
            break