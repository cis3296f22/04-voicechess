import unittest
import piece
import square
from typing import List


def test_initial_pawn_moves():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # testing bp moves at (1, 1)
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.Black, piece_type=piece.PieceType.Pawn, position=(1, 1))

    # initially pawn moves either one square forward or two squares forward
    expected_answer = [(1, 2), (1, 3)]

    # Check possible moves for black pawn located at (1,1)
    assert moving_piece.possible_moves(board) == expected_answer


def test_pawn_can_eat_move():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "  ", "bp", "bp", "bp", "bp", "bp"],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "bp", "  ", "  ", "  ", "  ", "  "],
        ["  ", "wp", "  ", "  ", "  ", "  ", "  ", "  "],  # testing wp moves at (1, 4)
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wp", "  ", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.White, piece_type=piece.PieceType.Pawn, position=(1, 4))

    # White pawn eats black pawn diagonally and can also move forward
    expected_answer = [(1, 3), (2, 3)]

    # Check possible moves for white pawn located at (1,4)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


def test_rook_moves():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "  ", "bp", "bp", "bp", "bp", "bp"],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "bp", "  ", "  ", "  ", "  ", "  "],
        ["  ", "wp", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wp", "  ", "wp", "wp", "wp", "wp", "wp", "  "],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],  # testing wr moves at (7, 7)
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.White, piece_type=piece.PieceType.Rook, position=(7, 7))

    # White rook moves either vertically or horizontally until it faces an obstacle
    # can_eat (7, 1)
    # can_move (7, 6), (7, 5), (7, 4), (7, 3), (7, 2)
    expected_answer = [(7, 1), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2)]

    # Check possible moves for white rook located at (7,7)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


def test_knight_moves():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "  ", "bp", "bp", "  ", "bp", "bp"],
        ["  ", "  ", "  ", "  ", "  ", "bp", "  ", "  "],
        ["  ", "  ", "bp", "  ", "  ", "  ", "  ", "  "],
        ["  ", "wp", "  ", "  ", "  ", "  ", "wn", "  "],  # testing moves of wn at (6, 4)
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wp", "  ", "wp", "wp", "wp", "wp", "wp", "  "],
        ["wr", "wn", "wb", "wq", "wk", "wb", "  ", "wr"],
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.White, piece_type=piece.PieceType.Knight, position=(6, 4))

    # White knight moves in an L-shape
    # can_eat (5, 2)
    # can_move (7, 2), (4, 3), (4, 5), (7, 6)
    expected_answer = [(5, 2), (7, 2), (4, 3), (4, 5), (7, 6)]

    # Check possible moves for white knight located at (6,4)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


def test_bishop_moves():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "  ", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "  ", "  ", "bp", "  ", "bp", "bp"],
        ["  ", "  ", "  ", "bp", "  ", "bp", "  ", "  "],
        ["  ", "  ", "bp", "  ", "  ", "bb", "  ", "  "],  # testing moves of bb at (5,3)
        ["  ", "wp", "  ", "  ", "  ", "  ", "wn", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wp", "  ", "wp", "wp", "wp", "wp", "wp", "  "],
        ["wr", "wn", "wb", "wq", "wk", "wb", "  ", "wr"],
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.Black, piece_type=piece.PieceType.Bishop, position=(5, 3))

    # Black bishop moves diagonally
    # can_eat (6, 4), (2, 6)
    # can_move (2,0), (3, 1), (4, 2), (6, 2), (4, 4), (3, 5), (2, 6)
    expected_answer = [(6, 4), (2, 6), (2, 0), (3, 1), (4, 2), (6, 2), (4, 4), (3, 5), (2, 6)]

    # Check possible moves for black bishop located at (5,3)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


def test_king_moves():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "  ", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "  ", "  ", "bp", "  ", "bp", "bp"],
        ["  ", "  ", "bp", "bp", "  ", "bp", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "bb", "  ", "  "],
        ["  ", "wp", "  ", "  ", "wp", "  ", "wn", "  "],
        ["  ", "  ", "  ", "  ", "wk", "  ", "  ", "  "],  # testing moves of wk at (4,5)
        ["wp", "  ", "wp", "wp", "  ", "wp", "wp", "  "],
        ["wr", "wn", "wb", "wq", "  ", "wb", "  ", "wr"],
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.White, piece_type=piece.PieceType.King, position=(4, 5))

    # White king moves one step in all directions
    # can_eat
    # can_move (3, 4), (3, 5), (4, 6), (5, 5), (5, 4)
    expected_answer = [(3, 4), (3, 5), (4, 6), (5, 5), (5, 4)]

    # Check possible moves for white king located at (4,5)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


def test_queen_moves():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "  ", "  ", "bk", "bb", "bn", "br"],
        ["bp", "bp", "  ", "  ", "bp", "  ", "bp", "bp"],
        ["  ", "  ", "  ", "bp", "  ", "bp", "  ", "  "],
        ["  ", "  ", "bp", "bq", "  ", "bb", "  ", "  "],  # testing moves of bq at (3,3)
        ["  ", "wp", "  ", "  ", "wp", "  ", "wn", "  "],
        ["  ", "  ", "  ", "  ", "wk", "  ", "  ", "  "],
        ["wp", "  ", "wp", "wp", "  ", "wp", "wp", "  "],
        ["wr", "wn", "wb", "wq", "  ", "wb", "  ", "wr"],
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.Black, piece_type=piece.PieceType.Queen, position=(3, 3))

    # Black queen moves diagonally + vertically + horizontally
    # can_eat (4, 4), (0, 6), (3, 6)
    # can_move (5, 1), (2, 2), (4, 2), (4, 3), (2, 4), (3, 4), (1, 5), (3, 5)
    expected_answer = [(4, 4), (0, 6), (3, 6), (5, 1), (2, 2), (4, 2), (4, 3), (2, 4), (3, 4), (1, 5), (3, 5)]

    # Check possible moves for black queen located at (3,3)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


def test_king_avoids_getting_in_checkmate():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "  ", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "  ", "  ", "bp", "  ", "bp", "bp"],
        ["  ", "  ", "  ", "bp", "  ", "bp", "  ", "  "],
        ["  ", "  ", "bp", "  ", "  ", "bb", "  ", "  "],
        ["  ", "wp", "  ", "  ", "wp", "  ", "wn", "  "],
        ["  ", "  ", "  ", "  ", "wk", "  ", "  ", "  "],  # testing moves of wk at (4,5)
        ["wp", "  ", "wp", "wp", "  ", "wp", "wp", "  "],
        ["wr", "wn", "wb", "wq", "  ", "wb", "  ", "wr"],
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.White, piece_type=piece.PieceType.King, position=(4, 5))

    # White king moves one step in all directions
    # Initially, wk can_move (3, 4), (5, 5), (3, 5), (4, 6), (5, 4)
    # But wk can_be_checked if it moves to (3, 4) so we can't move to that positions
    expected_answer = [(3, 5), (4, 6), (5, 5), (5, 4)]

    # Check possible moves for white king located at (4,5)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


def test_pawn_can_cover_check():
    # Set up board
    board: List['square.Square']
    position = [
        ["br", "bn", "bb", "  ", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "  ", "bp", "bp", "bp"],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "bq", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "bq"],
        ["  ", "  ", "  ", "  ", "  ", "wp", "  ", "  "],
        ["wp", "wp", "wp", "wp", "wp", "  ", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],  # test pawn move at (6, 6)
    ]
    board = [["  " for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j] = square.Square(i, j)

    for i in range(8):
        for j in range(8):
            if position[i][j].strip():
                board[j][i].set_piece(
                    piece.Piece.from_short_anotation(position[i][j], (j, i))
                )

    # Set up piece to move
    moving_piece = piece.Piece(color=piece.PieceColor.White, piece_type=piece.PieceType.Pawn, position=(6, 6))

    # Pawn can cover check
    # can_move (6, 5)
    expected_answer = [(6, 5)]

    # Check possible moves for white pawn located at (6, 6)
    assert set(moving_piece.possible_moves(board)) == set(expected_answer)


if __name__ == '__main__':
    unittest.main()