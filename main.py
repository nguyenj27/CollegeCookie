from flask import Flask, render_template, request
app = Flask(__name__)

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