from piece import Piece


class Square:
    def __init__(self, row: int, col: int, rect=None, piece=None):
        self.containsPiece =  piece != None
        self.piece = piece
        self.col = col
        self.row = row
        self.position = (row,col)
        self.rect = rect
    def set_piece(self, piece: Piece):
        if not piece:
            return
        self.piece = piece
        self.containsPiece = True
    
    def has_piece(self):
        return self.containsPiece



