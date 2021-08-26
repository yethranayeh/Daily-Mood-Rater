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
    with connection:
        cursor.execute("""CREATE TABLE moods (
            mood INTEGER,
            description TEXT,
            date TEXT
            )""")

    # connection.commit()

def save_values(mood:int, description=""):
    with connection:
        cursor.execute("SELECT date FROM moods WHERE date = :date", {"date":str(datetime.now())[:10]})
        # If there is no entry matching the current date:
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO moods VALUES (:mood, :desc, :date)", 
                {"mood":mood, "desc":description, "date":str(datetime.now())[:10]})
        else:
            # If an entry for current date exists, let the method of the app know by returning 0 to indicate failure
            return 0

    # connection.commit()

def update_values(mood:int, description=""):
    with connection:
        cursor.execute("""UPDATE moods 
                        SET mood = :mood,
                            description = :desc,
                        WHERE date = :today""",
                        {"mood":mood, "desc":description, "today":str(datetime.now())[:10]})

def show_values():
    cursor.execute("SELECT * FROM moods")
    result = cursor.fetchall()

    return result

try:
    create_table()
except sqlite3.OperationalError as err:
    pass
except Exception as err:
    print("\033[1;37;40mPreviously uncaught exception for creating table, if you are a user please let me know about this:")
    print("\033[1;31;40m", err, "\033[0;37;40m")

