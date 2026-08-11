from flask import Flask, jsonify, request
import json
from pathlib import Path

app = Flask(__name__)

USERS_FILE = Path(__file__).parent / "users.json"


def load_users():
    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


@app.get("/users")
def get_users():
    return jsonify(load_users())


@app.get("/users/<int:user_id>")
def get_user(user_id):

    users = load_users()

    for user in users:
        if user["id"] == user_id:
            return jsonify(user)

    return jsonify({"message": "User not found"}), 404


@app.post("/users")
def create_user():

    users = load_users()

    data = request.get_json()

    if users:
        next_id = max(user["id"] for user in users) + 1
    else:
        next_id = 1

    data["id"] = next_id

    users.append(data)

    save_users(users)

    return jsonify(data), 201

@app.put("/users/<int:user_id>")
def update_user(user_id):

    users = load_users()

    data = request.get_json()

    for user in users:
        if user["id"] == user_id:
            user.update(data)
            save_users(users)
            return jsonify(user)

    return jsonify({"message": "User not found"}), 404


@app.delete("/users/<int:user_id>")
def delete_user(user_id):

    users = load_users()

    for user in users:
        if user["id"] == user_id:

            users = [u for u in users if u["id"] != user_id]

            save_users(users)

            return jsonify(
                {
                    "message": "User deleted successfully"
                }
            )

    return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)