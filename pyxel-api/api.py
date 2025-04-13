# api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import create_table, insert_player, update_score, get_top_players,player_exists

app = Flask(__name__)
CORS(app)

create_table()

@app.route("/")
def index():
    return "API IshinoAme en ligne", 200


@app.route("/submit-score", methods=["POST"])
def submit_score():
    data = request.get_json()
    username = data.get("username")
    score = data.get("score")

    if not username or not isinstance(score, int):
        return jsonify({"error": "Invalid data"}), 400
    
    insert_player(username)
    update_score(username, score)
    return jsonify({"message": "Score updated"}), 200

@app.route("/top", methods=["GET"])
def top():
    top_players = get_top_players()
    return jsonify(top_players), 200

@app.route("/check-username/<username>", methods=["GET"])
def check_username(username):
    if player_exists(username):
        return jsonify({"available": False}), 200
    else:
        return jsonify({"available": True}), 200


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
