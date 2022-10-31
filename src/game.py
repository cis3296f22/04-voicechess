from typing import List
import pygame as pg
from piece import Piece
from square import Square


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800,600))
        self.dark_square_color = (0, 0, 255)
        self.light_square_color = (255, 255, 255)
        self.board: List['Square']
        self.running = True

    def render(self):
        pg.display.flip()

    def start(self):
        self.create_board()
        self.add_pieces()
        self.render()
        self.main()
        pass

    def create_board(self):
        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
                color = self.light_square_color
                isBlack = (i + j) % 2 == 0
                if isBlack:
                    color = self.dark_square_color

                self.board[i].append(Square( i,j, pg.draw.rect(self.screen, color, [i * 75, j*75, 75, 75])))
        return self.board

    def add_pieces(self, pos=None):
        # TODO: position reading
        if pos:
            return
        pos = [
            "br", "bn", "bb", "bq", "bk", "bb", "bn", "br",
            "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",
            "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
            "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
            "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
            "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
            "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp",
            "wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr",
        ]

        for i in range(8):
            for j in range(8):
                if pos[(i * 8) + j] != "  ":
                    self.board[j][i].set_piece(
                        Piece.from_short_anotation( pos[(i * 8)+j], (j,i))
                    )
        self.draw_pieces()

    def draw_pieces(self):
        self.images = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].has_piece():
                    img = pg.image.load(self.board[i][j].piece.image)
                    img = pg.transform.scale(img, (75,75))
                    rect = img.get_rect()
                    rect.topleft = (i *75, j * 75)
                    self.board[i][j].piece.rect = rect

                    self.board[i][j].piece.blit_image = img

                    self.screen.blit(img, (i*75,j*75))

    def main(self):
        moving = False
        moving_piece = None
        while self.running:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False

                if ev.type == pg.MOUSEBUTTONDOWN:
                    for i in range(8):
                        for j in range(8):
                            sqr = self.board[i][j]
                            if sqr.rect.collidepoint(ev.pos) and sqr.has_piece() :
                                pg.draw.rect(self.screen, (255,0,0), sqr, 5)
                                moving = True
                                moving_piece = sqr.piece
                                break

                elif ev.type == pg.MOUSEBUTTONUP:
                    moving = False
                    moving_piece = None
                    pass
                
                elif ev.type == pg.MOUSEMOTION and moving :
                    moving_piece.rect.move_ip(ev.rel)
            if moving and moving_piece:
                self.screen.blit( moving_piece.blit_image , moving_piece.rect)
            self.add_pieces()
            pg.display.update()
            
           
            
            