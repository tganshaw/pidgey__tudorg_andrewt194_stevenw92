from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import sqlite3
import blog
import user

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DB_CURSOR = DB.cursor()

DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS userdata(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS blogdata(blog_name TEXT, blog_id INTEGER PRIMARY KEY AUTOINCREMENT, user INT, entries INT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS entrydata(blog_id INT, text TEXT, entry_id INT);")

app = Flask(__name__)

app.secret_key = "ttestingtestingnotfinalresult"

@app.route("/profile")
def homepage():
    if 'username' not in session:
        return render_template("login.html")

    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()

    DB_CURSOR.execute(f"SELECT id FROM userdata WHERE username =\"{session['username']}\";")
    userId = DB_CURSOR.fetchone()[0]
    session['userId'] = userId
    numBlogs = blog.get_num_blogs(userId)
    arr = blog.get_blog_links(userId)
    return render_template("userprofile.html", username = session["username"], numblogs = numBlogs, blogs = blog.get_blogs(userId), txt = arr, owner = "true")

#----------------------------------------------------------

@app.route("/blog", methods = ["POST","GET"])
def blogpage():
    if("blog_id" not in request.args):
        return redirect("/")
    blog_name = blog.get_blog_name(request.args["blog_id"])
    blogVar = blog.load_blog(request.args["blog_id"])
    blogOwner = "false"
    if('username' in session):
        if(user.get_username(blog.get_blog_owner(request.args["blog_id"])) == session['username']):
            blogOwner = "true"
    entries = ""
    for i in range(len(blogVar)):
        entries += blogVar[i][0]
        if blogOwner == "true":
            #entries+="<br>"
            blog_id = request.args["blog_id"]
            entries+=f"<a href = /edit?editing=true&blog_id={blog_id}&entry_id={i}> edit this entry</a>"
        entries +="<br>"

    return render_template("blog.html", txt = entries, blog_id = request.args["blog_id"], owner = blogOwner, blog_title = blog_name)

#----------------------------------------------------------

@app.route("/edit", methods = ["POST","GET"])
def edit():
    blogTitle = ""
    if not 'username' in session:
        return redirect("/")
    if("blog_id" in request.args):
        blogTitle = blog.get_blog_name(request.args["blog_id"])
        if("entry_id" in request.args):
            txt = blog.get_entry(request.args['blog_id'], request.args["entry_id"])[0]
            return render_template("edit.html", editing = request.args['editing'], title = blogTitle, blog_id = request.args['blog_id'], entry_id = request.args["entry_id"], txt = txt)
        return render_template("edit.html", editing = request.args['editing'],title = blogTitle, blog_id = request.args['blog_id'], entry_id = -1)
    return render_template("edit.html", editing = request.args['editing'], title = blogTitle)

#----------------------------------------------------------

@app.route("/add", methods = ["POST","GET"])
def add():
    if not 'username' in session:
        return redirect("/")
    blogId = 0;
    if(not "blog_id" in request.args):
        if(request.args['title'] == "" or request.args["title"] == " "):
            return render_template("edit.html", editing = "false", titleerror = "Title Can't Be Empty")
        if(request.args['body'] == "" or request.args["body"] == " "):
            return render_template("edit.html", editing = "false", bodyerror = "Body Can't Be Empty")
        blog.create_blog(request.args['title'], session['userId'])
        blogId = blog.get_blog_id(request.args['title'],session['userId'])
        blog.create_entry(blogId,request.args['body'])
    else:
        blogTitle = blog.get_blog_name(request.args['blog_id'])
        if(request.args['body'] == "" or request.args["body"] == " "):
            return render_template("edit.html", editing = "true", title = blogTitle, blog_id = request.args["blog_id"], bodyerror = "Body Can't Be Empty", entry_id = request.args["entry_id"])
        blogId = request.args['blog_id']
        if(request.args['entry_id'] != "-1"):
            print(request.args['entry_id'])
            blog.edit_entry(request.args['body'], blogId, request.args['entry_id'])
        else:
            blog.create_entry(blogId, request.args['body'])
    return redirect(f"/blog?blog_id={blogId}")

#----------------------------------------------------------

@app.route("/viewuser", methods=["POST","GET"])
def viewuser():
    if 'username' in request.args:
        userName = request.args["username"]
        if userName == "":
            userName = '%'
        user_list = user.find_user(userName)
        if len(user_list) == 0:
            return render_template("homepage.html", user_error = "No such users exist")
        txt = ""
        for i in range(len(user_list)):
            txt+=f'<a href = "/access?username={user_list[i][0]}">{user_list[i][0]}</a><br>'
        return render_template("search_results.html", txt = txt)
    else:
        redirect("/access")

#----------------------------------------------------------

@app.route("/viewblog",methods = ["POST","GET"])
def viewblog():
    if 'blog_title' in request.args:
        blog_name = request.args["blog_title"]
        if blog_name == "":
            blog_name = "%"
        blog_list = blog.find_blog(blog_name)
        if len(blog_list) == 0:
            return render_template("homepage.html", blog_error = "No such blogs exist")
        txt = ""
        for i in range(len(blog_list)):
            blog_id = blog_list[i][1]
            blog_title = blog_list[i][0]
            user_name = user.get_username(blog_list[i][2])
            txt+=f"<a href = '/blog?blog_id={blog_id}'>{blog_title}</a>"
            txt+=" by "
            txt+=f"<a href = '/access?username={user_name}'> {user_name} </a>"
            txt+="<br>"
        return render_template("search_results.html",txt = txt)
    return redirect("/")

#----------------------------------------------------------

@app.route("/access")
def access():
    if 'username' in request.args:
        userName = request.args['username']
        userId = user.get_user_id(userName)
        numBlogs = blog.get_num_blogs(userId)
        arr = blog.get_blog_links(userId)
        blogOwner = str('username' in session and session['username'] == userName).lower()
        print(blogOwner)
        return render_template("userprofile.html", username = userName, numblogs = numBlogs , blogs = blog.get_blogs(userId), txt = arr, owner = blogOwner)
    else:
        if 'username' in session:
            userName = session['username']
            userId = user.get_user_id(userName)
            numBlogs = blog.get_num_blogs(userId)
            arr = blog.get_blog_links(userId)
            return render_template("userprofile.html", username = userName, numblogs = numBlogs , blogs = blog.get_blogs(userId), txt = arr, owner = "true")
        return redirect("/")

#----------------------------------------------------------

@app.route("/")
def homepagehtml():
    loggedIn = "false"
    if 'username' in session:
        loggedIn = "true"
        DB = sqlite3.connect(DB_NAME)
        DB_CURSOR = DB.cursor()
        DB_CURSOR.execute(f"SELECT id FROM userdata WHERE username =\"{session['username']}\";")
        userId = DB_CURSOR.fetchone()[0]
        session['userId'] = userId
    else:
        return redirect("/login.html")
    return render_template("homepage.html",logged_in = loggedIn)

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
    if('username' in session): # If not coming from login page or if already logged in
        return redirect("/")

    userName = request.form['username']
    temp = ""
    for i in userName:
        if i != '"':
            temp += i
    userName = temp
    if(len(userName) < 1):
        return render_template("register.html", username_error = "Please enter a valid username")

    USER_DB = sqlite3.connect(DB_NAME)
    USER_DB_CURSOR = USER_DB.cursor()

    USER_DB_CURSOR.execute(f"SELECT COUNT(*) FROM userdata WHERE username = '{userName}';")
    alreadyExists = USER_DB_CURSOR.fetchone()[0]
    if(alreadyExists != 0):
        return render_template("register.html", username_error = "Username already taken")


    INSERT_STRING = f"INSERT INTO userdata VALUES(\"{userName}\",\"{request.form['password']}\", NULL);"
    USER_DB_CURSOR.execute(INSERT_STRING)
    print(request.form['username'] + ", " + request.form['password'] + ", " + INSERT_STRING)
    session['username'] = userName

    USER_DB.commit()
    USER_DB.close()
    return redirect("/")

#----------------------------------------------------------

@app.route("/login", methods = ["POST", "GET"])
def login():
    if('username' in session): # If not coming from login page or if already logged in
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
    return redirect("/login.html")


app.debug = True
app.run()
