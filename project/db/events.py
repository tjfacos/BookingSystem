from db.connection import *
from datetime import datetime

def CreateEvent(user):
    db, cursor = CreateConnection()

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    cursor.execute("INSERT INTO Events (eventID, attendee_no, host, public, name, created) VALUES (UUID(), %s, %s, %s, %s, %s)", (
        0,
        user["user_id"],
        False,
        "My Event",
        time
    ))

    db.commit()

    cursor.execute(f"SELECT eventID FROM Events WHERE created = '{time}'")
    id = cursor.fetchone()[0]

    return id

def EventBelongsToUser(id, user):
    db, cursor = CreateConnection()

    cursor.execute(f"SELECT host FROM Events WHERE eventID = '{id}'")
    host = cursor.fetchone()[0]

    # print(type(host))
    # print(type(user["user_id"]))

    if user["user_id"] == host:
        return True
    
    return False










