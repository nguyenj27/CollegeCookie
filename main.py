import re
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Day
from twilio.rest import TwilioRestClient
import datetime

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

    user = session.query(User).filter_by(
        name=login_session["username"]).one()

    login_session["user_id"] = user.id
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


def printUserInfo():
    print "user_id: ", login_session["user_id"]
    print "user name: " , login_session["username"]


def getTime(minutes):
    hour = str(minutes/60)
    minute = str(minutes % 60)
    ampm = ""
    if hr<3:
        ampm = "P.M"
    if hr>7:
        ampm = "A.M"

    concat = 



    hour = str(hour)
    minute = str(minute)


@app.route('/data')
def data():

    printUserInfo()
    error = {}

    print("/data")
    users = session.query(User).filter_by(school_name=login_session["school"]).all()

    userAvailableDays = []
    usertimes = session.query(Day).filter_by(user_id=login_session["user_id"])
    for a in usertimes:
        userAvailableDays.append(a.day)

    now = datetime.datetime.today().weekday() - 3
    matching = []
    usr = {}
    if now in userAvailableDays:
        user_time = session.query(Day).filter_by(user_id=login_session[
            "user_id"], day=now).one()
        users_times = session.query(Day).filter_by(day=now).all()
        print login_session["user_id"]
        print "current day: ", now

        for t in users_times:
            if abs(t.time - user_time.time) <= 40:
                user = session.query(User).filter_by(id=t.user_id).one()
                usr["name"] = user.name
                usr["school_name"] = user.school_name
                usr["profile"] = user.profile
                usr["phone_number"] = user.phone_number
                usr["time"] = getTime(t.time)
                usr["bio"] = user.bio
                matching.append(dict(usr))

                print "available user: ", user.name
    else:
        error["noMatching"] = "You don't have any matching schedule today!"


    return render_template('matching2.html', matching=matching)


@app.route('/jen')
def jen():

    users = session.query(User).all()

    return render_template('matching.html', users=users)


@app.route("/seeding")
def three():
    session.add(User(name="orange", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/profile.png",
                     phone_number="2247300978",
                     bio = "hi"))


    session.add(User(name="apple", password="123", school_name="Depaul",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "Just started at UIC"))


    session.add(User(name="banana", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "I love birds"))

    session.add(User(name="oxygen", password="123", school_name="Depaul",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "I sleep with a giant peeps pillow"))


    session.add(User(name="nitrogen", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "Reed <333"))

    session.add(User(name="steak", password="123", school_name="Depaul",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "Wildhacks is making me sleepy"))

    session.add(User(name="fish", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "Milkshakes from Potbelly's"))

    session.add(Day(time=12 * 60 + 30, day=1, available_location="library",
                    user_id=2))

    session.add(
        Day(time=12 * 60 + 30, day=2, available_location="student center",
            user_id=2))

    session.add(Day(time=11 * 60, day=3, available_location="student center",
                    user_id=2))

    session.add(Day(time=11 * 60 + 30, day=1, available_location="student "
                                                                 "center",
                    user_id=2))

    session.add(Day(time=11 * 60, day=2, available_location="student center",
                    user_id=1))

    session.add(Day(time=11 * 60, day=3, available_location="student center",
                    user_id=1))

    session.add(Day(time=11 * 60, day=4, available_location="student center",
                    user_id=1))

    session.add(Day(time=11 * 60, day=1, available_location="library",
                    user_id=3))

    session.add(Day(time=11*60, day=2, available_location="cafeteria",
                    user_id=2))
    session.add(Day(time=11 * 60 + 30, day=1, available_location="cafeteria",
                    user_id=4))

    session.add(Day(time=12*60, day=2, available_location="A-20", user_id=4))

    session.add(Day(time=11*60, day=2, available_location="Cafeteria",
                    user_id=5))

    session.commit()

    return redirect(url_for('data'))


@app.route("/twilio")
def twilio():
    # q = session.query(User)
    # users = session.query(User).all()
    # print users
    return render_template('twilio.html')
    # return q.column_descriptions

@app.route("/twilio", methods = ["POST"])
def twilio_post():
    account_sid = "AC7d5c71c0797a0aa04f9f1efcd6c15e05"
    auth_token = "cdf9182e972608bc41a94145bfe22667"
    fromnumber = "+12244780132 "
    tonumber = "+17733296548"
    body_text = "Kappa"
    client = TwilioRestClient(account_sid, auth_token)
    _body = request.form['text']
    message = client.messages.create(
    to="+17733296547",
    from_="+12244780132",
    body=_body)
    return "Message successfully sent!"
#     # print(message.sid)



if __name__ == "__main__":
    app.run()
    app.secret_key = 'supersecretkey'
    app.debug = True
