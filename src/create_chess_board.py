import chess
import chess.svg


board = chess.Board("7k/4KP2/4p2p/p6P/Pp3P2/8/P1pr4/6R1 b - - 0 38")
with open("output/board.svg", "w") as f:
    f.write(chess.svg.board(board))