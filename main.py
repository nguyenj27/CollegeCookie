import re
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from database_setup import Base, User, Day
from twilio.rest import TwilioRestClient
import datetime

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
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



@app.route("/currentUser")
def whoami():
    if 'username' in login_session:
        time = session.query(Day).filter_by(day = datetime.datetime.today(

        ).weekday()).one()

        return login_session["username"], time


@app.route('/login', methods=['POST'])
def doLogin():
    if 'username' in login_session:
        return redirect(url_for('data'))

    ret = session.query(exists().where(User.name == request.form["username"]
                                   )).scalar()
    if ret:
        print "ret: ", ret
        login_session["username"] = request.form["username"]
        login_session["password"] = request.form["password"]

        user = session.query(User).filter_by(
            name=login_session["username"]).one()

        login_session["user_id"] = user.id
        login_session["school"] = "UIC"


        return redirect(url_for('data'))
    else:
        print "the user name does not exist"
        return render_template('login.html', messege="The user does not exist")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        school = request.form["school_name"]
        phone_number = request.form["phone_number"]

        user = User(name=username,
                    password=password,
                    school_name=school,
                    phone_number=phone_number)

        session.add(user)
        session.commit()

        login_session["username"] = username
        login_session["password"] = password
        user = session.query(User).filter_by(
            name=login_session["username"]).one()

        print "this is the signup route"
        login_session["user_id"] = user.id
        # No matter what user input for the school, we make them go to UIC lol.
        login_session["school"] = "UIC"

        return render_template('buttons.html')
        # save the user information to the database.
    else :
        return render_template('signup.html')

def printUserInfo():
    print "user_id: ", login_session["user_id"]
    print "user name: " , login_session["username"]


def getTime(minutes):
    hour = minutes/60
    minute = minutes % 60
    hour_string = str(hour)
    minute_string = str(minute)
    if(minute_string == '0'):
        minute_string = '00'
    if hour<3:
        ampm = "P.M"
    if hour>7:
        ampm = "A.M"

    concat = hour_string + ":" + minute_string + " " + ampm
    print concat
    return concat


@app.route('/data')
def data():
    printUserInfo()
    error = {}
    userAvailableDays = []

    usertimes = session.query(Day).filter_by(user_id=login_session["user_id"])
    for a in usertimes:
        userAvailableDays.append(a.day)

    now = datetime.datetime.today().weekday()

    print "now: ", now
    matching = []
    usr = {}
    if now in userAvailableDays:
        user_time = session.query(Day).filter_by(user_id=login_session[
            "user_id"], day=now).one()
        users_times = session.query(Day).filter_by(day=now).all()
        print login_session["user_id"]
        print "current day: ", now

        for t in users_times:
            if abs(t.time - user_time.time) <= 40 and t.user_id != \
                    login_session["user_id"]:

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


@app.route('/setTimes', methods=["GET", "POST"])
def setTimes():
    if request.method == 'POST':
        for key, value in request.form.iteritems():
            minutes = float(value) * 60
            day = key

            session.add(Day(time=minutes, day=day,
                            user_id=login_session["user_id"]))

            session.commit()

        return redirect(url_for('data'))
    if request.method == 'GET':
        return render_template('buttons.html')



@app.route("/seeding")
def three():


    session.add(User(name="Seho", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/seho.jpg",
                     phone_number="2247300978",
                     bio = "Just started at UIC"))


    session.add(User(name="Jennifer", password="123", school_name="Depaul",
                     legal_name="jen",
                     profile="./static/images/jen.jpg",
                     phone_number="2247300978",
                     bio = "I love birds"))

    session.add(User(name="Elona", password="123", school_name="Depaul",
                     legal_name="seho",
                     profile="./static/images/elona.jpg",
                     phone_number="2247300978",
                     bio = "I sleep with a giant peeps pillow"))


    session.add(User(name="Jorge", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/jorge.jpg",
                     phone_number="2247300978",
                     bio = "Reed <333"))

    session.add(User(name="steak", password="123", school_name="Depaul",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "Wildhacks is making me sleepy"))



    session.add(User(name="steak", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/profile.png", phone_number="2247300978",
                     bio = "Milkshakes from Potbelly's"))

    session.add(User(name="fish", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/profile.png",
                     phone_number="2247300978",
                     bio="Milkshakes from Potbelly's"))


    session.add(User(name="apple", password="123", school_name="UIC",
                     legal_name="seho",
                     profile="./static/images/profile.png",
                     phone_number="2247300978",
                     bio="Milkshakes from Potbelly's"))



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



    session.add(Day(time=12 * 60, day=6, available_location="Cafeteria",
                    user_id=1))

    session.add(Day(time=12 * 60, day=6, available_location="Cafeteria",
                    user_id=2))

    session.add(Day(time=12 * 60, day=6, available_location="Cafeteria",
                    user_id=3))

    session.add(Day(time=12 * 60, day=6, available_location="Cafeteria",
                    user_id=4))

    session.add(Day(time=12 * 60, day=6, available_location="Cafeteria",
                    user_id=5))

    session.add(Day(time=12 * 60, day=6, available_location="Cafeteria",
                    user_id=6))

    session.add(Day(time=12 * 60, day=6, available_location="Cafeteria",
                    user_id=7))


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
