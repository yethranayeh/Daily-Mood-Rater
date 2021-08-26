import sqlite3
from datetime import datetime

try:
    connection = sqlite3.connect("mood.db")
    connected = True
except Exception as err:
    print("\033[1;31;40mThe application faced a problem while trying to create or connect to the database.\033[0;37;40m")
    connected = False
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
    cursor.execute(f"INSERT INTO moods VALUES ({mood}, '{description}', '{str(datetime.now())[:19]}')")
    connection.commit()

def show_values():
    cursor.execute("SELECT * FROM moods")
    result = cursor.fetchall()
    return result

try:
    create_table()
except sqlite3.OperationalError as err:
    pass

