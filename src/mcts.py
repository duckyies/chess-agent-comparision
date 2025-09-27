import chess
import math
import random
from board import evaluate_board
class MCTSNode:
    def __init__(self, board: chess.Board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = list(board.legal_moves)

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.41):
        """UCT selection"""
        choices = [
            (child.wins / child.visits) +
            c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices.index(max(choices))]

class MCTS:
    def __init__(self, board: chess.Board, side: bool, n_simulations: int = 1000, rollout_depth: int = 20):
        self.board = board
        self.side = side
        self.n_simulations = n_simulations
        self.rollout_depth = rollout_depth
        self.movesAnalyzed = 0   

    def _select(self, node: MCTSNode):
        while not node.board.is_game_over() and node.is_fully_expanded():
            node = node.best_child()
        return node

    def _expand(self, node: MCTSNode):
        if not node.untried_moves:
            return node
        move = node.untried_moves.pop()
        board_copy = node.board.copy()
        board_copy.push(move)
        self.movesAnalyzed += 1  
        child = MCTSNode(board_copy, parent=node, move=move)
        node.children.append(child)
        return child

    def _simulate(self, board: chess.Board):
        """
        Play heuristic-guided simulation instead of random moves.
        """
        score = self.heuristic_rollout(board, self.side, depth=self.rollout_depth)
        return score / 1000  # normalize to ~0-1 for backpropagation

    def _backpropagate(self, node: MCTSNode, result: float):
        while node:
            node.visits += 1
            if node.board.turn != self.side:
                node.wins += result
            else:
                node.wins += (1 - result)
            node = node.parent

    def getBestMove(self):
        root = MCTSNode(self.board.copy())

        for _ in range(self.n_simulations):
            node = self._select(root)
            if not node.board.is_game_over():
                node = self._expand(node)
            result = self._simulate(node.board.copy())
            self._backpropagate(node, result)

        if not root.children:
            return None
        best = max(root.children, key=lambda c: c.visits)
        return best.move

    def makeBestMove(self):
        move = self.getBestMove()
        if move:
            self.board.push(move)
        return move


    def evaluate_board_after_move(self, board: chess.Board, move: chess.Move, side: bool) -> int:
        board.push(move)
        score = evaluate_board(board, side)
        board.pop()
        return score

    def heuristic_rollout(self, board: chess.Board, side: bool, depth: int = 10) -> int:
        """
        Play a short simulation (depth moves) using simple heuristics instead of random moves.
        Return the evaluation score from `side`'s perspective.
        """
        current_board = board.copy()
        
        for _ in range(depth):
            if current_board.is_game_over():
                break
            
            legal_moves = list(current_board.legal_moves)
            # Heuristic sorting: captures > checks > promotion > others
            legal_moves.sort(key=lambda move: (
                1000 if current_board.is_capture(move) else 0,
                500 if current_board.gives_check(move) else 0,
                self.evaluate_board_after_move(current_board, move, side)
            ), reverse=True)

            # Pick the top 1–2 moves randomly
            top_moves = legal_moves[:2]
            move = random.choice(top_moves)
            current_board.push(move)
            self.movesAnalyzed += 1   # count every heuristic-guided move
        # Return heuristic evaluation at the end of the rollout
        return evaluate_board(current_board, side)
