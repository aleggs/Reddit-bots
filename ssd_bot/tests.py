import sqlite3

db = sqlite3.Connection("comments.db")

print(db.execute('''SELECT * FROM comments;''').fetchall())