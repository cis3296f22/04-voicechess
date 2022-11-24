from enum import Enum
from typing import Tuple

from square import Square
def get_color_moves(board, color):
    all_oposite_moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j].has_piece() and board[i][j].piece.color == color:
                all_oposite_moves.append( board[i][j].piece.possible_moves(board))
    return all_oposite_moves

class PieceType (Enum):
    Rook = 0,
    Bishop = 1,
    Knight = 2,
    King = 3,
    Queen = 4,
    Pawn = 5


class PieceColor(Enum):
    Black = 0,
    White = 1


class Piece:
    def __init__(self, color: PieceColor, piece_type: PieceType, position: Tuple['int'],  rect=None) -> None:
        self.color = color
        self.piece_type = piece_type
        self.short_annotation = "w" if self.color == PieceColor.White else "b"
        self.rect = rect
        self.position: Tuple['int'] = position

        match piece_type:
            case PieceType.Rook:
                self.short_annotation += 'r'
            case PieceType.Bishop:
                self.short_annotation += 'b'
            case PieceType.Knight:
                self.short_annotation += 'n'
            case PieceType.Queen:
                self.short_annotation += 'q'
            case PieceType.Pawn:
                self.short_annotation += 'p'
            case PieceType.King:
                self.short_annotation += 'k'
        self.image = f'images/pieces/{self.short_annotation}.png'

        self.alive = True

    def from_short_anotation(short_annotation: str, position):
        if len(short_annotation) != 2:
            return

        piece_type = None
        color = PieceColor.White if short_annotation[0] == 'w' else PieceColor.Black

        match short_annotation[1]:
            case 'b':
                piece_type = PieceType.Bishop
            case 'r':
                piece_type = PieceType.Rook
            case 'n':
                piece_type = PieceType.Knight
            case 'k':
                piece_type = PieceType.King
            case 'q':
                piece_type = PieceType.Queen
            case 'p':
                piece_type = PieceType.Pawn
        p = Piece(color, piece_type, position)

        return p

    def possible_moves(self, board, should_filter=True):
        moves = []
        match self.piece_type:
            case PieceType.Pawn:
                moves = self.__get_pawn_moves(board)
            case PieceType.Queen:
                moves = self.__get_queen_moves(board)
            case PieceType.King:
                moves = self.__get_king_moves(board)
            case PieceType.Rook:
                moves = self.__get_rook_moves(board)
            case PieceType.Knight:
                moves = self.__get_knight_moves(board)
            case PieceType.Bishop:
                moves = self.__get_bishop_moves(board)

        return self.__filter_moves_that_put_king_in_check__(moves, board) if should_filter else moves

    def __get_pawn_moves(self, board):
        (row, col) = self.position
        all_posible = []
        eat_moves = []
        res = []

        if self.color == PieceColor.Black:
            all_posible = [(row, col + 1)]
            eat_moves = [(row - 1, col + 1), (row + 1, col + 1)]
            if self.position[1] == 1:
                all_posible.append((row, col + 2))

        else:
            all_posible = [(row, col - 1)]
            eat_moves = [(row + 1, col - 1), (row - 1, col - 1)]
            if self.position[1] == 6:
                all_posible.append((row, col - 2))

        for move in eat_moves:
            (r, c) = move
            if r not in range(0, 8) or c not in range(0, 8):
                continue
            sqr = board[r][c]

            if sqr.has_piece() and sqr.piece.color != self.color:
                res.append(move)

        for move in all_posible:
            (row, col) = move

            if row not in range(0, 8) or col not in range(0, 8):
                continue

            sqr = board[row][col]
            if sqr.has_piece():
                continue
            else:
                res.append(move)

        return res

    def __get_rook_moves(self, board):
        axes = [
            (1,  0),
            (-1, 0),
            (0,  1),
            (0, -1)
        ]
        res = []
        (row, col) = self.position

        for ax in axes:
            new_row = row + ax[0]
            new_col = col + ax[1]
            while new_row in range(0, 8) and new_col in range(0, 8):
                sqr = board[new_row][new_col]
                if sqr.has_piece():
                    if sqr.piece.color == self.color:
                        break
                    else:
                        res.append((new_row, new_col))
                        break
                else:
                    res.append((new_row, new_col))
                new_row += ax[0]
                new_col += ax[1]

        return res

    def __get_bishop_moves(self, board):
        axes = [
            (1,  1),
            (1, - 1),
            (- 1,  -1),
            (-1, 1)
        ]
        res = []
        (row, col) = self.position

        for ax in axes:
            new_row = row + ax[0]
            new_col = col + ax[1]
            while new_row in range(0, 8) and new_col in range(0, 8):
                sqr = board[new_row][new_col]
                if sqr.has_piece():
                    if sqr.piece.color == self.color:
                        break
                    else:
                        res.append((new_row, new_col))
                        break
                else:
                    res.append((new_row, new_col))
                new_row += ax[0]
                new_col += ax[1]

        return res

    def __get_knight_moves(self, board):
        (row, col) = self.position
        all_possibles = [
            # row 2
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),

            # column 2
            (row + 1, col - 2), (row - 1, col - 2),
            (row + 1, col + 2), (row - 1, col + 2),
        ]
        res = []
        for move in all_possibles:
            (row, col) = move

            if row not in range(0, 8) or col not in range(0, 8):
                continue

            sqr = board[row][col]
            if sqr.has_piece():
                if sqr.piece.color == self.color:
                    continue
                else:
                    res.append(move)
            else:
                res.append(move)

        return res

    def __get_king_moves(self, board):
        (row, col) = self.position

        all_possible_moves = [
            (row + 1, col + 1), (row + 1, col), (row + 1, col - 1),
            (row, col + 1), (row, col - 1),
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)
        ]
        res = []
        for move in all_possible_moves:
            (row, col) = move

            if row not in range(0, 8) or col not in range(0, 8):
                continue

            sqr = board[row][col]
            if sqr.has_piece():
                if sqr.piece.color == self.color:
                    continue
                else:
                    res.append(move)
            else:
                res.append(move)
        # get all opposite move to check if the square we are going to does not put us in check

        
        return res

    def __get_queen_moves(self, board):
        return self.__get_bishop_moves(board) + self.__get_rook_moves(board)

    def __copy_board__(self, board):
        new_board = [[ "  " for _ in range(8) ] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                new_board[i][j] = Square(i, j, None, board[i][j].piece)
        return new_board

    def __filter_moves_that_put_king_in_check__(self, moves, board):

        opposite_color = PieceColor.Black if self.color == PieceColor.White else PieceColor.White

        opposite_color_pieces = []
        my_pieces = []
        my_king = ""
        

        for i in range(8):
            for j in range(8):
                if board[i][j].has_piece():
                    if board[i][j].piece.color == opposite_color:
                        opposite_color_pieces.append(board[i][j].piece)
                    else:
                        if board[i][j].piece.piece_type == PieceType.King:
                            my_king = board[i][j].piece
                        my_pieces.append(board[i][j].piece)
                    

        res = []

        # find out if piece is blocking a check
        # find out if piece is 

        for move in moves:
            (r,c) = move
            new_board = self.__copy_board__(board)

            # makes move
            new_board[self.position[0]][self.position[1]].piece = None
            new_board[r][c].piece = self

            should_break = False


            # for each piece the opponent has
            for op_piece in opposite_color_pieces:
                # print(f"checking {op_piece.short_annotation}")
                if should_break:
                    break
                # for every possible move that piece has check if that move touches our king
                for poss_move in op_piece.possible_moves(new_board, False):
                    if self.piece_type == PieceType.King:
                        if move == poss_move:
                            should_break = True
                            break
                    if poss_move == my_king.position and op_piece.position not in self.possible_moves(board, False):
                        should_break = True
                        break
            
            if not should_break:
                res.append(move)

        return res
