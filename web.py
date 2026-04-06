from flask import Flask, render_template, request, redirect, url_for
import json
import os
import asyncio

app = Flask(__name__)

# ---------------------
# Simple login system
# ---------------------
USERNAME = "jer"
PASSWORD = "jer"  # Change this to something secure

# ---------------------
# Load/save banned words
# ---------------------
def load_banned_words():
    if not os.path.exists("banned_words.json"):
        with open("banned_words.json", "w") as f:
            json.dump({"words": []}, f)
    with open("banned_words.json", "r") as f:
        return json.load(f)["words"]

def save_banned_words(words):
    with open("banned_words.json", "w") as f:
        json.dump({"words": words}, f)

# ---------------------
# Load strikes
# ---------------------
def load_strikes():
    if not os.path.exists("strikes.json"):
        with open("strikes.json", "w") as f:
            json.dump({}, f)
    with open("strikes.json", "r") as f:
        return json.load(f)

# ---------------------
# Load logs
# ---------------------
def load_logs():
    if not os.path.exists("logs.json"):
        return []
    with open("logs.json", "r") as f:
        return json.load(f)

# ---------------------
# Routes
# ---------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("dashboard"))
    return '''
        <h2>Login</h2>
        <form method="post">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    banned_words = load_banned_words()
    strikes = load_strikes()
    logs = load_logs()

    if request.method == "POST":
        if "add_word" in request.form:
            word = request.form.get("add_word").lower()
            if word not in banned_words:
                banned_words.append(word)
                save_banned_words(banned_words)
        elif "remove_word" in request.form:
            word = request.form.get("remove_word").lower()
            if word in banned_words:
                banned_words.remove(word)
                save_banned_words(banned_words)

    banned_list_html = "<br>".join(banned_words)
    strikes_html = "<br>".join([f"{k}: {v}" for k,v in strikes.items()])
    logs_html = "<br>".join([f"{l['user']} ({l['type']}): {l['message']}" for l in logs])

    return f'''
        <h2>Dashboard</h2>
        <h3>Banned Words</h3>
        {banned_list_html}
        <form method="post">
            Add word: <input name="add_word">
            <input type="submit" value="Add">
        </form>
        <form method="post">
            Remove word: <input name="remove_word">
            <input type="submit" value="Remove">
        </form>
        <h3>User Strikes</h3>
        {strikes_html}
        <h3>Logs</h3>
        {logs_html}
    '''

# ---------------------
# Run dashboard
# ---------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
