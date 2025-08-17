import chess
import math
import random
from minmax import *
from board import *

class AI:
    def __init__(self, board: chess.Board, side: bool, depth: int = 3):
        self.board = board
        self.side = side
        self.depth = depth
        self.movesAnalyzed = 0

    def _move_sort_key(self, move: chess.Move):
        return (
            self.board.is_capture(move),
            self.board.gives_check(move),
            move.promotion is not None,
        )

    def _min_max_alpha_beta(self, depth: int, alpha: int, beta: int) -> int:
        if depth == 0 or self.board.is_game_over():
            return evaluate_board(self.board, self.side)

        maximizing = (self.board.turn == self.side)
        legal_moves = list(self.board.legal_moves)
        legal_moves.sort(key=self._move_sort_key, reverse=True)

        if maximizing:
            value = -math.inf
            for move in legal_moves:
                self.board.push(move)
                self.movesAnalyzed += 1
                value = max(value, self._min_max_alpha_beta(depth - 1, alpha, beta))
                self.board.pop()
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = math.inf
            for move in legal_moves:
                self.board.push(move)
                self.movesAnalyzed += 1
                value = min(value, self._min_max_alpha_beta(depth - 1, alpha, beta))
                self.board.pop()
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
        
    def _min_max(self, depth: int) -> int:
        if depth == 0 or self.board.is_game_over():
            return evaluate_board(self.board, self.side)

        maximizing = (self.board.turn == self.side)
        legal_moves = list(self.board.legal_moves)
        legal_moves.sort(key=self._move_sort_key, reverse=True)

        if maximizing:
            value = -math.inf
            for move in legal_moves:
                self.board.push(move)
                self.movesAnalyzed += 1
                value = max(value, self._min_max(depth - 1))
                self.board.pop()
            return value
        else:
            value = math.inf
            for move in legal_moves:
                self.board.push(move)
                self.movesAnalyzed += 1
                value = min(value, self._min_max(depth - 1))
                self.board.pop()
            return value


    def getBestMove(self) -> chess.Move:
        best_value = -math.inf
        best_moves = []

        legal_moves = list(self.board.legal_moves)
        legal_moves.sort(key=self._move_sort_key, reverse=True)

        for move in legal_moves:
            self.board.push(move)
            value = self._min_max_alpha_beta(self.depth - 1, -math.inf, math.inf)
            self.board.pop()

            if value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)
        
        if not best_moves:
            return None
        
        return random.choice(best_moves)

    def makeBestMove(self) -> chess.Move:
        move = self.getBestMove()
        if not move:
            return
        self.board.push(move)
        return move