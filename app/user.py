import sqlite3

DB_NAME = "Data/database.db"

def get_username(user_id):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT username FROM userdata WHERE id = {user_id};")
    cursorfetch = cursor.fetchone()[0]
    db.commit()
    db.close()
    return cursorfetch

def get_user_id(username):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM userdata WHERE username = \"{username}\";")
    cursorfetch = cursor.fetchone()[0]
    db.commit()
    db.close()
    return cursorfetch
