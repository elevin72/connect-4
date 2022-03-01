import pygame as pg
import sys
from board import *
from abminimax import *
import time
from guiPlayer import *
from aiPlayer import *

BLACK = (0,0,0)
GREY = (152, 158, 158)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRID_HEIGHT = 300
GRID_WIDTH = 350
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
DEPTH=2

global SCREEN, CLOCK
pg.init()
SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pg.time.Clock()
SCREEN.fill(GREY)

def get_player() -> tuple[Player, Player]:
    r = pg.Rect(0, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT)
    y = pg.Rect(WINDOW_WIDTH/2, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT)
    pg.draw.rect(SCREEN, RED, r)
    pg.draw.rect(SCREEN, YELLOW, y)
    pg.display.update()
    def done(human, ai):
        SCREEN.fill(GREY)
        pg.display.update()
        return human,ai
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if (pos[0] > 0 and pos[0] < WINDOW_WIDTH/2 and
                    pos[1] > 0 and pos[1] < WINDOW_HEIGHT
                    ):
                    human = GuiPlayer((WINDOW_HEIGHT, WINDOW_WIDTH), 'X')
                    ai = AiPlayer(DEPTH, 'O')
                    return done(human, ai)
                elif (pos[0] > WINDOW_WIDTH/2 and pos[0] < WINDOW_WIDTH and
                    pos[1] > 0 and pos[1] < WINDOW_HEIGHT
                    ):
                    human = GuiPlayer((WINDOW_HEIGHT, WINDOW_WIDTH), 'O')
                    ai = AiPlayer(DEPTH, 'X')
                    return done(human, ai)

def do_game_over(board: Board):
    board.print()
    print("game over")
    if board.end_state == EndState.X_WIN:
        print("X/Red Won!")
    if board.end_state == EndState.O_WIN:
        print("O/Yellow Won!")
    if board.end_state == EndState.TIE:
        print("Its a tie!")

def drawGrid():
    blockSize = 50 #Set the size of the grid block
    for x in range(25, GRID_WIDTH, blockSize):
        for y in range(25, GRID_HEIGHT, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(SCREEN, BLACK, rect, 1)


def drawCircles(b):
    for i,row in enumerate(b.board):
        for j,space in enumerate(row):
            if space == 'X':
                pg.draw.circle(SCREEN, RED, ((j+1)*50, (i+1)*50), 20)
            if space == 'O':
                pg.draw.circle(SCREEN, YELLOW, ((j+1)*50, (i+1)*50), 20)


def main():
    board = Board()
    human,ai = get_player()
    while True:
        drawGrid()
        drawCircles(board)
        pg.display.update()
        if board.game_over():
            do_game_over(board)
            time.sleep(3)
            exit()
        if board.turn == ai.color:
            minimax_value, board = ai.play(board)
            board.print()
            print('Value:', minimax_value)
            print('Heuristic Value:', board.evaluate())
        else:
            board = human.play(board)
            board.print()
            print('Heuristic Value:', board.evaluate())


if __name__ == '__main__':
    main()
