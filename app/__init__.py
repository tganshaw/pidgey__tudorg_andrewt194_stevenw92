from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import sqlite3
import blog

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DB_CURSOR = DB.cursor()

DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS userdata(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS blogdata(blog_name TEXT, blog_id INTEGER PRIMARY KEY AUTOINCREMENT, user INT, entries INT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS entrydata(blog_id INT, text TEXT, entry_id INT);")

app = Flask(__name__)

app.secret_key = "ttestingtestingnotfinalresult"

@app.route("/")
def homepage():
    if 'username' not in session:
        return render_template("login.html")

    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()

    DB_CURSOR.execute(f"SELECT id FROM userdata WHERE username =\"{session['username']}\";")
    userId = DB_CURSOR.fetchone()[0]
    session['userId'] = userId
    DB_CURSOR.execute(f"SELECT COUNT(*) FROM blogdata WHERE user = {userId};")
    numBlogs = DB_CURSOR.fetchone()[0]
    arr = ""
    for i in blog.get_blogs(userId):
        blogTitle = i[0]
        blogId = i[1]
        arr+= f"<a href = /blog?blog_id={blogId}>{blogTitle}</a><br>"
    return render_template("userprofile.html", username = session["username"], numblogs = numBlogs, blogs = blog.get_blogs(userId), txt = arr)

#----------------------------------------------------------

@app.route("/blog", methods = ["POST","GET"])
def blogpage():
    blogVar = blog.load_blog(request.args["blog_id"])
    entries = ""
    for entry in blogVar:
        entries += entry[0]
        entries +="<br>"
    return render_template("blog.html", txt = entries, blog_id = request.args["blog_id"])

#----------------------------------------------------------

@app.route("/edit", methods = ["POST","GET"])
def edit():
    blogTitle = ""
    if not 'username' in session:
        return redirect("/")
    if("blog_id" in request.args):
        blogTitle = blog.get_blog_name(request.args["blog_id"])
        return render_template("edit.html", editing = request.args['editing'],title = blogTitle, blog_id = request.args['blog_id'])
    return render_template("edit.html", editing = request.args['editing'], title = blogTitle)

#----------------------------------------------------------

@app.route("/add", methods = ["POST","GET"])
def add():
    if not 'username' in session:
        return redirect("/")
    blogId = 0;
    if(not "blog_id" in request.args):
        blog.create_blog(request.args['title'], session['userId'])
        blogId = blog.get_blog_id(request.args['title'],session['userId'])
        blog.create_entry(blogId,request.args['body'])
    else:
        blogId = request.args['blog_id']
        blog.create_entry(blogId, request.args['body'])
    return redirect(f"/blog?blog_id={blogId}")

#----------------------------------------------------------

@app.route("/login.html")
def loginhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("login.html")

#----------------------------------------------------------

@app.route("/register.html")
def registerhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("register.html")

#----------------------------------------------------------

@app.route("/register", methods = ["POST", "GET"])
def register():
    if((not request.args and not request.form) or 'username' in session): # If not coming from login page or if already logged in
        return redirect("/")

    USER_DB = sqlite3.connect(DB_NAME)
    USER_DB_CURSOR = USER_DB.cursor()

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

#----------------------------------------------------------

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

#----------------------------------------------------------

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


app.debug = True
app.run()
