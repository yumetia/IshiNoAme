# api.py
from flask import Flask, request, jsonify
from database import create_table, insert_player, update_score, get_top_players

app = Flask(__name__)
create_table()

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

if __name__ == "__main__":
    app.run(debug=True)
