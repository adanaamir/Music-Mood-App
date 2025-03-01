from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake user data (in real-world apps, this would come from a database)
users = {
    "adan": "password123",
    "user1": "mypassword"
}

@app.route("/login", methods=["POST"])
def login():
    data = request.json  # Get data from frontend
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)
