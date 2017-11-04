import re
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

####################
# TO DO
# 1. validate the username and password
# 2. work on the front end part of the code.


# just for temporary

engine = create_engine('sqlite:///main.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def main():
    return "maidfn page"


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/logout")
def logout():
    login_session.clear()
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def doLogin():
    print request.form["username"]
    login_session["username"] = request.form["username"]
    login_session["password"] = request.form["password"]
    login_session["school"] = "UIC"

    return render_template('page.html', username=login_session["username"],
                           password=login_session["password"], school=login_session["school"] )


@app.route('/signup', methods=['POST'])
def signUp():
    print "singup page."
    username = request.form["username"]
    password = request.form["password"]
    school = request.form["school_name"]

    user = User(name=username,
                password=password,
                school_name=school)

    session.add(user)
    session.commit()

    login_session["username"] = username
    login_session["password"] = password
    return render_template('page.html')
    # save the user information to the database.

@app.route('/data')
def data():
    print("/data")
    users = session.query(User).order_by(asc(User.id))
    return render_template('users.html', users=users)


@app.route("/seeding")
def three():

    session.add(User(name="orange", password="123", school_name="UIC",
                     breakfast=8*60*60))
    session.add(User(name="apple", password="123", school_name="UIC",
                     breakfast=7*60*60 + 30*60))
    session.add(User(name="banana", password="123", school_name="UIC",
                     breakfast=8*60*60 + 20*60))
    session.add(User(name="oxygen", password="123", school_name="UIC",
                     breakfast=9*60*60))
    session.add(User(name="nitrogen", password="123", school_name="UIC",
                     breakfast=9*60*60 + 10*60))
    session.add(User(name="steak", password="123", school_name="UIC",
                     breakfast=9*60*60 + 30*60))
    session.add(User(name="fish", password="123", school_name="UIC",
                     breakfast=10*60*60 + 10*60))

    session.commit()

    return redirect(url_for('data'))


@app.route("/4")
def four():
    return "4!"




if __name__ == "__main__":
    app.run()
    app.secret_key = 'supersecretkey'
    app.debug = True