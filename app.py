from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS = [
    "Basketball",
    "Soccer",
    "Badminton",
]

@app.route("/")
def index():
    return render_template("index.html", sport=SPORTS)

@app.route("/register", methods=["POST"]) #when this route is called, call this file
def register():
    if not request.form.get("name") or not request.form.get("sport"):
        return render_template("failure.html")
    return render_template("success.html")

app.config["TEMPLATES_AUTO_RELOAD"] = True
