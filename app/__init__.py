from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import sqlite3

DB_NAME = "app/Data/database.db"

app = Flask(__name__)

app.secret_key = "ttestingtestingnotfinalresult"

@app.route("/")
def homepage():
    if 'username' not in session:
        return render_template("register.html")
    USER_DB = sqlite3.connect(DB_NAME)
    USER_DB_CURSOR = USER_DB.cursor()

    USER_DB_CURSOR.execute(f"SELECT id FROM userdata WHERE username = \"{session['username']}\";")
    userId = USER_DB_CURSOR.fetchone()[0];
    USER_DB_CURSOR.execute(f"SELECT COUNT(*) FROM blogdata WHERE user = {userId};")
    numBlogs = USER_DB_CURSOR.fetchone()[0];
    return render_template("userprofile.html", username = session['username'], numblogs = numBlogs)

@app.route("/register.html")
def registerhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("register.html")

@app.route("/login.html")
def loginhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    if((not request.args and not request.form) or 'username' in session): # If not coming from login page or if already logged in
        return redirect("/")

    USER_DB = sqlite3.connect(DB_NAME)
    USER_DB_CURSOR = USER_DB.cursor()

    USER_DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS userdata(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

    USER_DB_CURSOR.execute(f"SELECT COUNT(*) FROM userdata WHERE username = '{request.form['username']}';")
    alreadyExists = USER_DB_CURSOR.fetchone()[0]
    if(alreadyExists != 0):
        return render_template("register.html", username_error = "Username already taken")


    INSERT_STRING = f"INSERT INTO userdata VALUES(\"{request.form['username']}\",\"{request.form['password']}\", NULL);"
    USER_DB_CURSOR.execute(INSERT_STRING)
    print(request.form['username'] + ", " + request.form['password'] + ", " + INSERT_STRING)
    session['username'] = request.form['username']

    USER_DB.commit()
    USER_DB.close()
    return redirect("/")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if((not request.args and not request.form) or 'username' in session): # If not coming from login page or if already logged in
        return redirect("/")
    USER_DB = sqlite3.connect(DB_NAME)
    USER_DB_CURSOR = USER_DB.cursor()

    USER_DB_CURSOR.execute(f"SELECT COUNT(*) FROM userdata WHERE username = '{request.form['username']}';")
    alreadyExists = USER_DB_CURSOR.fetchone()[0]
    if(alreadyExists == 0):
        return render_template("login.html", username_error = "User does not exist")
    USER_DB_CURSOR.execute(f"SELECT password FROM userdata WHERE username = '{request.form['username']}';")
    userPass = USER_DB_CURSOR.fetchone()[0]
    if(not userPass == request.form["password"]):
        return render_template("login.html", password_error = "Password is incorrect")
    session["username"] = request.form["username"]

    USER_DB.commit()
    USER_DB.close()

    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route("/displaydb") # testing only
def displaydb():
    TEST_DB = sqlite3.connect(DB_NAME)
    TEST_DB_CURSOR = TEST_DB.cursor()
    TEST_DB_CURSOR.execute("SELECT * FROM userdata")
    rows = TEST_DB_CURSOR.fetchall()
    for row in rows:
        print(row)

    TEST_DB.close()
    return "rows printed in terminal"

app.debug = True
app.run()
