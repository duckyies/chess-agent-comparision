import chess
import chess.engine
import chess.svg

from heuristics import *

WHITE = True
BLACK = False

PIECE_SQUARE_TABLES = {
    "pawns":    {WHITE: materialHeuristics["pawns"],    BLACK: mirror_table(materialHeuristics["pawns"])},
    "pawnsEnd": {WHITE: materialHeuristics["pawnsEnd"], BLACK: mirror_table(materialHeuristics["pawnsEnd"])},
    "knights":  {WHITE: materialHeuristics["knights"],  BLACK: mirror_table(materialHeuristics["knights"])},
    "bishops":  {WHITE: materialHeuristics["bishops"],  BLACK: mirror_table(materialHeuristics["bishops"])},
    "rooks":    {WHITE: materialHeuristics["rooks"],    BLACK: mirror_table(materialHeuristics["rooks"])},
    "queens":   {WHITE: materialHeuristics["queen"],   BLACK: mirror_table(materialHeuristics["queen"])},
    "kingMid":  {WHITE: materialHeuristics["kingStart"],  BLACK: mirror_table(materialHeuristics["kingStart"])},
    "kingEnd":  {WHITE: materialHeuristics["kingEnd"],  BLACK: mirror_table(materialHeuristics["kingEnd"])},
}


def evaluate_board(board: chess.Board, side: bool) -> int:
    """Evaluate board from perspective of 'side' using material + PSTs."""
    score = 0
    piece_map = board.piece_map()

    endgame = board.queens == 0 or len(piece_map) < 10

    for square, piece in piece_map.items():
        value = material_values[piece.piece_type]

        pst_value = 0
        if piece.piece_type == chess.PAWN:
            pst_value = PIECE_SQUARE_TABLES["pawnsEnd" if endgame else "pawns"][piece.color][square]
        elif piece.piece_type == chess.KNIGHT:
            pst_value = PIECE_SQUARE_TABLES["knights"][piece.color][square]
        elif piece.piece_type == chess.BISHOP:
            pst_value = PIECE_SQUARE_TABLES["bishops"][piece.color][square]
        elif piece.piece_type == chess.ROOK:
            pst_value = PIECE_SQUARE_TABLES["rooks"][piece.color][square]
        elif piece.piece_type == chess.QUEEN:
            pst_value = PIECE_SQUARE_TABLES["queens"][piece.color][square]
        elif piece.piece_type == chess.KING:
            pst_value = PIECE_SQUARE_TABLES["kingEnd" if endgame else "kingMid"][piece.color][square]

        piece_score = value + pst_value

        if piece.color == side:
            score += piece_score
        else:
            score -= piece_score

    return score