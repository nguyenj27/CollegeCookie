from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "don't eat lunch alone friend!"


@app.route("/login")
def login():
    return "this is the login page."

@app.route("/2")
def two():
    return "Hello World!"


@app.route("/3")
def three():
    return "Hello World!"


@app.route("/4")
def four():
    return "Hello World!"




