import chess
from minmax import *
from heuristics import *
from board import *
import time
import chess.svg
import chess.engine

if __name__ == "__main__":
    board = chess.Board()
    white_ai = AI(board, WHITE, depth=3)
    black_ai = AI(board, BLACK, depth=3)

    time_white = []
    time_black = []

    while not board.is_checkmate() and not board.is_fifty_moves():

        before_time = time.time()
        white_best_move = white_ai.makeBestMove()
        after_time = time.time()
        time_white.append(after_time - before_time)

        print(f"WHITE AI plays: {white_best_move}\n" )
        if not white_best_move:
            print("Game over")
            break

        print(board)
        
        before_time = time.time()
        black_best_move = black_ai.makeBestMove()
        after_time = time.time()
        time_black.append(after_time - before_time)
        
        print(f"BLACK AI plays: {black_best_move}\n")
        if not black_best_move:
            print("Game over")
            break

        print(board)

    print(f"\nBlack moves analyzed: {white_ai.movesAnalyzed}")
    print(f"White moves analyzed: {black_ai.movesAnalyzed}\n")

    print(f"\nAverage time taken per move for white - {sum(time_white)/len(time_white)}")
    print(f"Average time taken per move for black - {sum(time_black)/len(time_black)}\n")