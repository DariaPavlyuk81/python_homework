import sqlite3

# Connect to a new SQLite database
with  sqlite3.connect("../db/school.db") as conn:  # Create the file here, so that it is not pushed to GitHub!
    print("Database created and connected successfully.")
