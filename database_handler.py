# Module to handle database interactions, mainly for ToDo but could be used for others.


###############################
# ToDo
###############################
    

import sqlite3
with sqlite3.connect('example.db') as db:
        pass

class Databse_controller():
    """
    Class which handles database stuff. Objects are instantiated with table names
    so one object per table. 

    *Values*
    self.cursor = SQLite cursor
    self.db = SQLite db
    
    """
    def __init__(self, table_name):
        self.cursor = db.cursor()
        self.db = db



def ToDo_add(message, date, person, con):
    # Adds new entry to todo table.
    from datetime import datetime
    from random import randint

    id = randint(0, 2500)

    con.execute("""INSERT INTO ToDo(id, task, date, reminder_date)
    VALUES(?, ?, ?, ?)""", (id, message, (datetime.now), date))
    con.commit()
    return

