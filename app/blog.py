import os
import sqlite3
#Helper functions to add to flask app
#Can use them when manipulating db

DB_NAME = "Data/database.db"
db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

def load_blog(blog_id):
    DB_NAME = "Data/database.db"
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT text FROM entrydata WHERE blog_id = {blog_id};")
    db.commit()
    db.close()
    return cursor.fetchall()

def create_blog(blog_name, user):
    DB_NAME = "Data/database.db"
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS blogdata(TEXT blog_name, INTEGER PRIMARY KEY AUTOINCREMENT blog_id, INT user, INT entries);")
    cursor.execute(f'INSERT INTO blogdata("{blog_name}", NULL, {user}, 0);')
    db.commit()
    db.close()

def get_entry(blog_id, entry_id):
    DB_NAME = "Data/database.db"
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT text FROM entrydata WHERE blog_id = {blog_id} AND entry_id = {entry_id};")
    db.commit()
    db.close()
    return cursor.fetchone()

def create_entry(blog_id, txt):
    DB_NAME = "Data/database.db"
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS entrydata(INT blog_id, TEXT text, INT entry_id);")
    cursor.execute(f"SELECT entries FROM blogdata WHERE blog_id = {blog_id};")
    a = cursor.fetchone()
    entry_id = a[0]
    cursor.execute(f'INSERT INTO entrydata({blog_id}, "{txt}", {entry_id});')
    cursor.execute(f'UPDATE blogdata SET entries {entry_id+1} WHERE blog_id = {blog_id};')
    db.commit()
    db.close()

def edit_entry(txt, blog_id, entry_id):
    DB_NAME = "Data/database.db"
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f'UPDATE entrydata SET text = "{txt}" WHERE blog_id = {blog_id} AND entry_id = {entry_id}')
    db.commit()
    db.close()

def get_blog_id(blog_name, user):
    DB_NAME = "Data/database.db"
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f'SELECT blog_id FROM blogdata WHERE blog_name = "{blog_name}" AND user = {user};')
    db.commit()
    db.close()
    return cursor.fetchone()[0]

if __name__ == "__main__":
    create_blog("Andrew's blog", 9)
    create_entry(get_blog_id("Andrew's blog", 9), "hi entry added")
