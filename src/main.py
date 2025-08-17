import chess
from minmax import *
from heuristics import *
from board import *
import time
import chess.svg
import chess.engine
from chess import Termination 

if __name__ == "__main__":
    board = chess.Board()
    white_ai = AI(board, chess.WHITE, depth=2) 
    black_ai = AI(board, chess.BLACK, depth=3)

    time_white = []
    time_black = []

    while not board.is_game_over(): 
        if board.can_claim_draw():
            print("Draw claimed (fifty moves or threefold repetition)")
            break

        before_time = time.time()
        white_best_move = white_ai.makeBestMove()
        after_time = time.time()
        time_white.append(after_time - before_time)

        print(f"WHITE AI plays: {white_best_move}\n")
        if not white_best_move:
            print("Game over (no legal moves for White)")
            break

        print(board)
        
        if board.is_repetition(3):
            print("Draw by threefold repetition")
            break

        before_time = time.time()
        black_best_move = black_ai.makeBestMove()
        after_time = time.time()
        time_black.append(after_time - before_time)
        
        print(f"BLACK AI plays: {black_best_move}\n")
        if not black_best_move:
            print("Game over (no legal moves for Black)")
            break

        print(board)

        if board.is_repetition(3):
            print("Draw by threefold repetition")
            break

    outcome = board.outcome(claim_draw=True)  
    if outcome:
        if outcome.termination == Termination.CHECKMATE:
            winner = "White" if outcome.winner == chess.WHITE else "Black"
            print(f"Checkmate: {winner} wins")
        elif outcome.termination == Termination.STALEMATE:
            print("Draw by stalemate")
        elif outcome.termination == Termination.INSUFFICIENT_MATERIAL:
            print("Draw by insufficient material")
        elif outcome.termination == Termination.SEVENTYFIVE_MOVES:
            print("Draw by seventy-five moves rule")
        elif outcome.termination == Termination.FIVEFOLD_REPETITION:
            print("Draw by fivefold repetition")
        elif outcome.termination == Termination.FIFTY_MOVES:
            print("Draw by fifty moves rule (claimed)")
        elif outcome.termination == Termination.THREEFOLD_REPETITION:
            print("Draw by threefold repetition (claimed)")
        else:
            print("Game over (draw by other means)")
    else:
        print("Game over (undetermined outcome)")

    print(f"\nBlack moves analyzed: {white_ai.movesAnalyzed}")
    print(f"White moves analyzed: {black_ai.movesAnalyzed}\n")

    print(f"\nAverage time taken per move for white - {sum(time_white)/len(time_white)}")
    print(f"Average time taken per move for black - {sum(time_black)/len(time_black)}\n")
