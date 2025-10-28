import os
import sqlite3
#Helper functions to add to flask app
#Can use them when manipulating db

DB_NAME = "app/Data/database.db"
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
    cursor.execute("CREATE TABLE IF NOT EXISTS blogdata(blog_name TEXT, blog_id INTEGER PRIMARY KEY AUTOINCREMENT, user INT, entries INT);")
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
    entry_id = a[0]
    cursor.execute(f'INSERT INTO entrydata VALUES ({blog_id}, "{txt}", {entry_id});')
    cursor.execute(f'UPDATE blogdata SET entries = {entry_id+1} WHERE blog_id = {blog_id};')
    db.commit()
    db.close()

def edit_entry(txt, blog_id, entry_id):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f'UPDATE entrydata SET text = "{txt}" WHERE blog_id = {blog_id} AND entry_id = {entry_id}')
    db.commit()
    db.close()

def get_blog_id(blog_name, user):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f'SELECT blog_id FROM blogdata WHERE blog_name = "{blog_name}" AND user = {user};')
    cursorfetch = cursor.fetchone()
    db.commit()
    db.close()
    return cursorfetch[0]

if __name__ == "__main__":
    create_blog("Andrew's blog", 9)
    create_entry(get_blog_id("Andrew's blog", 9), "hi entry added")
