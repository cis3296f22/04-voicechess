from typing import List
import pygame as pg
from piece import Piece, PieceType, PieceColor
from square import Square


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800,600))
        self.dark_square_color = (0, 0, 255)
        self.light_square_color = (255, 255, 255)
        self.turn = PieceColor.White
        self.board: List['Square']
        self.position = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]
        self.running = True



    def start(self):
        self.draw_board()
        self.add_pieces()
        pg.display.flip()
        self.main()
        pass

    def draw_board(self):
        self.screen.fill((0,0,0))
        font = pg.font.SysFont('Anonymous Pro', 24)
        turn_str = "White's Turn" if self.turn == PieceColor.White else "Black's Turn" 
        text = font.render(turn_str,False, (255,255,255))
        self.screen.blit(text, (620,300))
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

    
    def print_position(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.position]))

    def add_pieces(self, pos=None):
        # TODO: position reading
        if pos:
            return

        for i in range(8):
            for j in range(8):
                if self.position[i][j].strip():
                    self.board[j][i].set_piece(
                        Piece.from_short_anotation( self.position[i][j], (j,i))
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
        moving_piece = None
        square_clicked = None
        while self.running:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False
                    return

                if ev.type == pg.MOUSEBUTTONDOWN:
                    should_break = False
                    for i in range(8):
                        if should_break:
                            break
                        for j in range(8):
                            sqr = self.board[i][j]

                            if sqr.rect.collidepoint(ev.pos) and sqr.has_piece() and sqr.piece.color == self.turn  :
                                # pg.draw.rect(self.screen, (255,0,0), sqr, 5)
                                moving_piece = sqr.piece
                                square_clicked = sqr
                                should_break = True
                                break
                elif ev.type == pg.MOUSEMOTION and moving_piece:
                    moving_piece.rect.move_ip(ev.rel)
                    self.draw_board()
                    self.screen.blit(moving_piece.blit_image, moving_piece.rect)


                elif ev.type == pg.MOUSEBUTTONUP:
                    
                                    
                    should_break = False
                    for i in range(8):
                        if should_break:
                            break
                        for j in range(8):
                            sqr = self.board[i][j]
                            if sqr.rect.collidepoint(ev.pos) and moving_piece and square_clicked :
                                self.position[j][i] = moving_piece.short_annotation
                                (y,z) = square_clicked.position
                                self.position[z][y] = "  "
                                should_break = True
                                self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
                                self.draw_board()
                                break
                    moving_piece = None
                # self.draw_board()
                self.add_pieces()
                pg.display.flip()
            
           
            
            