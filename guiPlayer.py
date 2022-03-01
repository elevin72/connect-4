from player import Player
import pygame as pg
import sys
import time


class GuiPlayer(Player):
    def __init__(self, window, color):
        super().__init__(color)
        self.w_height = window[0];
        self.w_width = window[1];
            
    def play(self, board):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if (board.turn == self.color and
                            pos[1] > 0 and pos[1] < self.w_height and
                            pos[0] > 0 and pos[0] < self.w_width):
                        move = ( pos[0] - 25 ) // 50
                        if board.is_legal_move(move):
                            return board.play(move)
            time.sleep(0.1)

