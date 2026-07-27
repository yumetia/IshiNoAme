from dotenv import load_dotenv
load_dotenv()

# api.py
import os
import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from database import create_table, create_player, get_password_hash, update_score, get_top_players, player_exists

app = Flask(__name__)
CORS(app)

create_table()

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")


def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        request.username = payload["username"]
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index():
    return "API IshinoAme en ligne", 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid data"}), 400

    if player_exists(username):
        return jsonify({"error": "Username already taken"}), 409

    password_hash = generate_password_hash(password)
    created = create_player(username, password_hash)
    if not created:
        return jsonify({"error": "Username already taken"}), 409

    token = generate_token(username)
    return jsonify({"token": token}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid data"}), 400

    password_hash = get_password_hash(username)
    if not password_hash or not check_password_hash(password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(username)
    return jsonify({"token": token}), 200


@app.route("/submit-score", methods=["POST"])
@token_required
def submit_score():
    data = request.get_json()
    score = data.get("score")

    if not isinstance(score, int):
        return jsonify({"error": "Invalid data"}), 400

    update_score(request.username, score)
    return jsonify({"message": "Score updated"}), 200


@app.route("/top", methods=["GET"])
def top():
    top_players = get_top_players()
    response = jsonify(top_players)
    response.headers["Cache-Control"] = "no-store"
    return response, 200


@app.route("/check-username/<username>", methods=["GET"])
def check_username(username):
    if player_exists(username):
        return jsonify({"available": False}), 200
    else:
        return jsonify({"available": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    