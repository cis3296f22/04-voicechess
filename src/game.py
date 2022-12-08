import threading
from time import sleep
from typing import List
import pygame as pg
from piece import Piece, PieceColor
from square import Square
import speech_recognition as sr
from speech import speak_to_move
import button
class Game:

   
        
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800,600))
        self.dark_square_color = "#769656"
        self.black_king: Square
        self.white_king: Square
        self.light_square_color = "#EEEED2"
        self.is_white_king_in_check = False
        self.is_black_king_in_check = False
        self.listeningResponse: str = "Not listening"
        self.turn = PieceColor.White
        self.listening = False
        self.checking_piece: Piece
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
        self.record_img = pg.image.load('images/button/rec.png').convert_alpha()
        self.record_button = button.Button(650, 400, self.record_img, 0.2)
        self.recording = False


    def play_move_voice(self, from_to:List):
        from_square_str = from_to[0]
        to_square_str = from_to[1]
            
        alphabet = 'abcdefgh'

        from_col =  alphabet.index( from_square_str[0].lower()) 
        from_row = 8 -   int(from_square_str[1]) 

        to_col =  alphabet.index( to_square_str[0].lower()) 
        to_row = 8 - int(to_square_str[1]) 


        print(f"from: {(from_col, from_row)} -> to: {(to_row, to_col)}, ")

        from_square: Square = self.board[from_col][from_row]
        to_square: Square = self.board[to_col][to_row]


        if not from_square.has_piece():
            return(f"THERE IS NO PIECE AT {from_square_str}")

        if from_square.piece.color != self.turn:
            return(f"wrong color/turn")

        if to_square.position not in from_square.piece.possible_moves(self.board):
            return(f"Piece on {from_square_str} can't move to {to_square_str}")
        
        self.position[from_row][from_col] = "  "
        self.position[to_row][to_col] = from_square.piece.short_annotation
        self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
        pg.mixer.music.play()

        self.add_pieces
        self.draw_game
        pg.display.flip()
        return f"Moved from {from_square_str} to {to_square_str} "
    def play_move(self, from_to:List):
        
        
            from_square_str = from_to[0]
            to_square_str = from_to[1]
                
            alphabet = 'abcdefgh'

            from_col =  alphabet.index( from_square_str[0].lower()) 
            from_row = 8 -   int(from_square_str[1]) 

            to_col =  alphabet.index( to_square_str[0].lower()) 
            to_row = 8 - int(to_square_str[1]) 


            print(f"from: {(from_col, from_row)} -> to: {(to_row, to_col)}, ")

            from_square: Square = self.board[from_col][from_row]
            to_square: Square = self.board[to_col][to_row]

            if not from_square.has_piece():
                return(f"THERE IS NO PIECE AT {from_square_str}")

            if to_square.position not in from_square.piece.possible_moves(self.board):
                return(f"Piece on {from_square_str} can't move to {to_square_str}")
            
            self.position[from_row][from_col] = "  "
            self.position[to_row][to_col] = from_square.piece.short_annotation
            self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
            pg.mixer.music.play()

        

            return f"Moved from {from_square_str} to {to_square_str} "

    def start(self):
        pg.mixer.music.load("sound.mp3")
        self.draw_game()
        self.add_pieces()
        pg.display.flip()
        self.main()
        # self.play_game_from_file('./src/game.txt')

    def get_color_pieces(self, color: PieceColor):
        pieces = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].has_piece() and self.board[i][j].piece.color == color:
                    pieces.append(self.board[i][j].piece)

        return pieces

    def get_color_moves(self, color: PieceColor):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].has_piece() and self.board[i][j].piece.color == color:
                    moves.append( self.board[i][j].piece.possible_moves(self.board))
        return moves

              
    def is_check_mate(self, king_in_check):
        moves = self.get_color_moves(king_in_check.piece.color) 
        return not any( moves )

    def update_check_status(self):
        kings = [self.white_king, self.black_king]
      
        for king in kings:
            all_oposite_moves = self.get_color_moves(PieceColor.Black if king.piece.color == PieceColor.White else PieceColor.White)

            did_break = False
            for piece_possible_moves in all_oposite_moves:
                if did_break:
                    break
                for move in piece_possible_moves:
                    
                    if move == king.piece.position:
                        pg.draw.rect(self.screen, (255,0,0), king, 5)
                        # self.checking_piece = piece
                        if king.piece.color == PieceColor.Black:
                            self.is_black_king_in_check = True
                            print("BLACK KING IN CHECK")
                            did_break = True
                            if self.is_check_mate(self.black_king):
                                self.running = False
                            break
                        else:
                            self.is_white_king_in_check = True
                            did_break = True
                            print("White KING IN CHECK")
                            if self.is_check_mate(self.white_king):
                                self.running = False
                            break
            if  did_break == False:
                if king.piece.color == PieceColor.Black:
                    self.is_black_king_in_check = False
                else:
                    self.is_white_king_in_check = False

    def draw_game(self):
        # PAINT THE ENTIRE SCREEN BLACK
        self.screen.fill((0,0,0))
        

        # RENDERS TURN TEXT
        font = pg.font.get_default_font()
        font = pg.font.SysFont(font, 26)
        turn_str = "White's Turn" if self.turn == PieceColor.White else "Black's Turn" 
        text = font.render(turn_str,False, (255,255,255))
        self.screen.blit(text, (620,300))

           # RENDERS LISTENING TEXT
        turn_str = self.listeningResponse 
        text = font.render(turn_str,False, (0,255,0))
        self.screen.blit(text, (610,500))

        self.board = [[ "  " for _ in range(8) ] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                color = self.light_square_color
                isBlack = (i  + (j + 1)) % 2 == 0
                if isBlack:
                    color = self.dark_square_color
                self.board[i][j] = Square( i,j, pg.draw.rect(self.screen, color, [i * 75, j*75, 75, 75]))



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
                    if self.position[i][j] == "wk":
                        self.white_king = self.board[j][i]
                    elif self.position[i][j] == "bk":
                        self.black_king = self.board[j][i]
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


        while self.running:
            if self.record_button.draw(self.screen):
                self.recording = True
                print("Listening")
                self.listeningResponse = "recording"
                command = speak_to_move()
                if command == False:
                    print("command not recognized")
                else:
                    voicemove = self.play_move_voice(command)
                    print(voicemove)
                self.recording = False
                print("done listening")
                self.listeningResponse = "not recording"
                self.draw_game()
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
                                
                                pg.draw.rect(self.screen, (255,255,0), sqr, 5)
                                moving_piece = sqr.piece
                                should_break = True
                                moves = moving_piece.possible_moves(self.board)

                                for move in moves:
                                    (r,c) = move
                                    possible_move_sqr = self.board[r][c]
                                    pg.draw.circle(self.screen, (150,150,150), possible_move_sqr.rect.center, 10)
                                break
                                
                        
                elif ev.type == pg.MOUSEMOTION and moving_piece:
                    self.draw_game()
                    moving_piece.rect.move_ip(ev.rel)
                    self.screen.blit(moving_piece.blit_image, moving_piece.rect)

                elif ev.type == pg.MOUSEBUTTONUP:
                    should_break = False
                    for i in range(8):

                        if should_break:
                            break
                        for j in range(8):
                            sqr = self.board[i][j]
                            if sqr.rect.collidepoint(ev.pos) and moving_piece :
                                if sqr.position not in moving_piece.possible_moves(self.board):
                                    self.draw_game()
                                    continue
                                
                                self.position[j][i] = moving_piece.short_annotation
                                (y,z) = moving_piece.position
                                self.position[z][y] = "  "
                                pg.mixer.music.play()
                                should_break = True
                                
                                self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
                                self.draw_game()
                                self.add_pieces()
                                self.update_check_status()
                                break
                    moving_piece = None

            self.add_pieces()
            pg.display.update()