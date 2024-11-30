from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import the CORS module
import time
from pathlib import Path
import sys

PARENT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PARENT_DIR))

from bot_logic import get_bot_move


app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)  # Enable CORS for all routes by default


@app.route('/')
def serve_index():
    """
    Serve the index.html page from the frontend directory.
    """
    return send_from_directory(app.static_folder, 'index.html')



@app.route('/api/move', methods=['POST'])
def get_move():
    """
    Handle requests from the frontend to get the bot's move.
    Expects a JSON payload with the current board state.
    """
    data = request.json
    board = data.get('board')  # Get the current board state from the request

    if board is None:
        return jsonify({"error": "Board state not provided"}), 400

    # Call the function to determine the bot's move
    col = get_bot_move(board)

    # It's unnerving if the bot plays so quickly
    time.sleep(1)

    # Return the bot's chosen column as a JSON response
    return jsonify({"column": col})

if __name__ == '__main__':
    app.run(debug=True)
