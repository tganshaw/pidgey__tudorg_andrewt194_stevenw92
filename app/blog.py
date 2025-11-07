import sqlite3
#Helper functions to add to flask app
#Can use them when manipulating db

DB_NAME = "Data/database.db"
db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

def load_blog(blog_id):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT text FROM entrydata WHERE blog_id = {blog_id};")
    cursorfetch = cursor.fetchall()
    db.commit()
    db.close()
    return cursorfetch

def create_blog(blog_name, user):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    x = ""
    for char in blog_name:
        if char != '"':
            x+=char
    blog_name = x
    cursor.execute("CREATE TABLE IF NOT EXISTS blogdata(blog_name TEXT, blog_id INTEGER PRIMARY KEY AUTOINCREMENT, user INT, entries INT);")
    cursor.execute(f'SELECT * FROM blogdata WHERE blog_name = "{blog_name}" AND user = {user};')
    a = cursor.fetchone()
    if a:
        return
    cursor.execute(f'INSERT INTO blogdata VALUES("{blog_name}", NULL, {user}, 0);')
    db.commit()
    db.close()

def get_entry(blog_id, entry_id):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT text FROM entrydata WHERE blog_id = {blog_id} AND entry_id = {entry_id};")
    cursorfetch = cursor.fetchone()
    db.commit()
    db.close()
    return cursorfetch

def create_entry(blog_id, txt):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS entrydata(blog_id INT, text TEXT, entry_id INT);")
    cursor.execute(f"SELECT entries FROM blogdata WHERE blog_id = {blog_id};")
    a = cursor.fetchone()
    if(not a):
        a = [0]
    entry_id = a[0]
    a = ""
    for char in txt:
        if char != '"':
            a+=char
    txt = a
    cursor.execute(f'INSERT INTO entrydata VALUES ({blog_id}, "{txt}", {entry_id});')
    cursor.execute(f'UPDATE blogdata SET entries = {entry_id+1} WHERE blog_id = {blog_id};')
    db.commit()
    db.close()

def edit_entry(txt, blog_id, entry_id):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    print(f'UPDATE entrydata SET text = "{txt}" WHERE blog_id = {blog_id} AND entry_id = {entry_id};')
    cursor.execute(f'UPDATE entrydata SET text = "{txt}" WHERE blog_id = {blog_id} AND entry_id = {entry_id};')
    db.commit()
    db.close()

def get_blog_id(blog_name, user):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    x = ""
    for char in blog_name:
        if char != '"':
            x+=char
    blog_name = x
    cursor.execute(f'SELECT blog_id FROM blogdata WHERE blog_name = "{blog_name}" AND user = {user};')
    cursorfetch = cursor.fetchone()
    db.commit()
    db.close()
    if not cursorfetch:
        return -1
    return cursorfetch[0]

def get_blogs(user):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM blogdata WHERE user = {user}')
    fetch = cursor.fetchall()
    db.commit()
    db.close()
    return fetch

def get_blog_name(blog_id):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f'SELECT blog_name FROM blogdata WHERE blog_id = {blog_id};')
    cursorfetch = cursor.fetchone()[0]
    db.commit()
    db.close()
    return cursorfetch

def get_blog_owner(blog_id):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f'SELECT user FROM blogdata WHERE blog_id = {blog_id};')
    cursorfetch = cursor.fetchone()[0]
    db.commit()
    db.close()
    return cursorfetch

def get_num_blogs(user):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM blogdata WHERE user = {user};")
    cursorfetch = cursor.fetchone()[0]
    db.commit()
    db.close()
    return cursorfetch

def get_blog_links(user):
    arr = ""
    for i in get_blogs(user):
        blogTitle = i[0]
        blogId = i[1]
        arr+= f"<a href = /blog?blog_id={blogId}>{blogTitle}</a><br>"
    return arr

def find_blog(string):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM blogdata WHERE blog_name LIKE '%{string}%';")
    cursorfetch = cursor.fetchall()
    db.commit()
    db.close()
    return cursorfetch

if __name__ == "__main__":
    create_blog("asd", 11)
