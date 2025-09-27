import time
import chess
from flask import Flask, render_template, jsonify, send_from_directory
from minmax import AI
from mcts import MCTS

app = Flask(__name__)

board = chess.Board()
white_ai = AI(board, chess.WHITE, depth=3)
black_ai = MCTS(board, chess.BLACK)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/img/<path:filename>")
def custom_static(filename):
    return send_from_directory("img", filename)

@app.route("/state")
def state():
    return jsonify({
        "fen": board.fen()
    })

@app.route("/move")
def move():
    if board.is_game_over():
        return jsonify({"fen": board.fen(), "done": True})

    if board.turn == chess.WHITE:
        white_ai.makeBestMove()
    else:
        black_ai.makeBestMove()

    return jsonify({
        "fen": board.fen(),
        "done": board.is_game_over()
    })

if __name__ == "__main__":
    app.run(debug=True)
