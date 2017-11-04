import re
from flask import Flask, render_template, request
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User

app = Flask(__name__)


####################
# TO DO
# 1. validate the username and password
# 2. work on the front end part of the code.


# just for temporary
userinfo = {}


engine = create_engine('sqlite:///flashcard.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

dbSession = DBSession()


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

    user = User(name=userinfo["username"], password=userinfo["password"],
          school_name="UIC")
    dbSession.add(user)
    print "added an user"

    return render_template('page.html', username=userinfo["username"],
                           password=userinfo["password"])



@app.route('/signup', methods=['POST'])
def signUp():
    print "singup page."
    username = request.form["username"]
    password = request.form["password"]

    userinfo["username"] = username
    userinfo["password"] = password

    return render_template('userinfo.html')
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