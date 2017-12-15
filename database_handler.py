# Module to handle database interactions, mainly for ToDo but could be used for others.


###############################
# ToDo
###############################

def ToDo_create_db(con):
    # This function has side effects, be careful.
    con.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(250) NOT NULL, date TEXT, reminder_date TEXT)")
    return

def ToDo_add(message, date, person, con):
    # This function has side effects, be careful.
    from datetime import datetime
    con.execute("""INSERT INTO ToDo(id, task, person, date, reminder_date)
    VALUES(?, ?, ?, ?, ?)""", (id, message, person, (datetime.now), date))
    con.commit()
    return

