from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import sqlite3

DB_NAME = "database.db"

app = Flask(__name__)

app.secret_key = "ttestingtestingnotfinalresult"

@app.route("/")
def homepage():
    if 'username' not in session:
        return render_template("register.html")
    return render_template("homepage.html",username = session['username'])

@app.route("/register", methods = ["POST", "GET"])
def register():
    if((not request.args and not request.form) or 'username' in session): # If not coming from login page or if already logged in
        return redirect("/")

    USER_DB = sqlite3.connect(DB_NAME)
    USER_DB_CURSOR = USER_DB.cursor()

    USER_DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS userdata(username TEXT, password TEXT);")

    INSERT_STRING = f"INSERT INTO userdata VALUES(\"{request.form['username']}\",\"{request.form['password']}\");"
    USER_DB_CURSOR.execute(INSERT_STRING)
    print(request.form['username'] + ", " + request.form['password'] + ", " + INSERT_STRING)
    session['username'] = request.form['username']

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
    rowString = ""
    for row in rows:
        rowString = rowString + row + "\n"

    TEST_DB.close()
    return rowString

app.debug = True
app.run()
