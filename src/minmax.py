import chess
import math
import random
from minmax import *  
from board import *
from heuristics import * 
import chess.polyglot

class AI:
    def __init__(self, board: chess.Board, side: bool, depth: int = 3):
        self.board = board
        self.side = side
        self.depth = depth
        self.movesAnalyzed = 0
        self.TT = {} 

    def quiescence(self, board: chess.Board, alpha: int, beta: int, is_maximizing: bool) -> int:
        stand_pat = evaluate_board(board, self.side) 

        if is_maximizing:
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
        else:
            if stand_pat <= alpha:
                return alpha
            if beta > stand_pat:
                beta = stand_pat

        legal_moves = [move for move in board.legal_moves if board.is_capture(move)]
        legal_moves.sort(key=lambda m: self._move_sort_key(m), reverse=True)

        for move in legal_moves:
            board.push(move)
            score = self.quiescence(board, alpha, beta, not is_maximizing)
            board.pop()

            if is_maximizing:
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
            else:
                if score <= alpha:
                    return alpha
                if score < beta:
                    beta = score

        return alpha if is_maximizing else beta

    def _move_sort_key(self, move: chess.Move):
        if self.board.is_capture(move):
            victim = self.board.piece_at(move.to_square)
            attacker = self.board.piece_at(move.from_square)
            if victim and attacker:
                return 10000 + (100 * material_values[victim.piece_type] - material_values[attacker.piece_type])
            return 10000
        if self.board.gives_check(move):
            return 5000
        return 0

    def minimax(self, board: chess.Board, depth: int, alpha: int, beta: int, is_maximizing: bool) -> int:
        if board.is_checkmate():
            return -999999 if board.turn == self.side else 999999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        if depth == 0 or board.is_game_over():
            return self.quiescence(board, alpha, beta, is_maximizing)

        key = (chess.polyglot.zobrist_hash(board), depth, board.turn)
        if key in self.TT:
            return self.TT[key]

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return evaluate_board(board, self.side)

        legal_moves.sort(key=lambda m: self._move_sort_key(m), reverse=True)

        if is_maximizing:
            value = -math.inf
            for move in legal_moves:
                board.push(move)
                score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()

                if score > value:
                    value = score
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    break
            self.TT[key] = value
            return value
        else:
            value = math.inf
            for move in legal_moves:
                self.movesAnalyzed += 1
                board.push(move)
                score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()

                if score < value:
                    value = score
                if value < beta:
                    beta = value
                if alpha >= beta:
                    break
            self.TT[key] = value
            return value

    def getBestMove(self) -> chess.Move:
        best_value = -math.inf
        best_moves = []

        legal_moves = list(self.board.legal_moves)
        legal_moves.sort(key=self._move_sort_key, reverse=True)

        for move in legal_moves:
            self.board.push(move)
            value = self.minimax(self.board, self.depth - 1, -math.inf, math.inf, False)
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
