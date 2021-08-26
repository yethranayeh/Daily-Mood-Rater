import sqlite3
from datetime import datetime

try:
    connection = sqlite3.connect("mood.db")
except Exception as err:
    print("\033[1;37;40mThe application faced a problem while trying to create or connect to the database:\033[0;37;40m")
    print("\033[1;31;40m", err, "\033[0;37;40m")
    import sys
    sys.exit()

cursor = connection.cursor()

def create_table():
    cursor.execute("""CREATE TABLE moods (
        mood INTEGER,
        description TEXT,
        date TEXT
        )""")

    connection.commit()

def save_values(mood:int, description=""):
    cursor.execute(
        "INSERT INTO moods VALUES (:mood, :desc, :date)", 
        {"mood":mood, "desc":description, "date":str(datetime.now())[:19]})

    connection.commit()

def show_values():
    cursor.execute("SELECT * FROM moods")
    result = cursor.fetchall()

    return result

try:
    create_table()
except sqlite3.OperationalError as err:
    pass

