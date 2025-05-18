import sqlite3

conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

print("connected to db/lessin/db")