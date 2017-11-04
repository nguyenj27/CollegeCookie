import re
from flask import Flask, render_template, request
app = Flask(__name__)


####################
# TO DO
# 1. validate the username and password
# 2. work on the front end part of the code.


# just for temporary
userinfo = {}

@app.route("/")
def main():
    return "maidfn page"


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def doLogin():
    print request.form["username"]
    userinfo["username"] = request.form["username"]
    userinfo["password"] = request.form["password"]
    return render_template('userinfo.html', username=userinfo["username"],
                           password=userinfo["password"])


@app.route('/signup', methods=['POST'])
def signUp():
    print "singup page."
    username = request.form["username"]
    password = request.form["password"]

    # check if the username already exist
    # validateUsername(username)
    # validagte the password
    # validatePassword(password)

    userinfo["username"] = username
    userinfo["password"] = password

    # save the user information to the database.


@app.route("/3")
def three():
    return "3"


@app.route("/4")
def four():
    return "4!"


if __name__ == "__main__":
    app.run()
    app.secret_key = 'supersecretkey'
    app.debug = True