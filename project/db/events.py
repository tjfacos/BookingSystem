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
    try:
        host = cursor.fetchone()[0]
    except TypeError:
        return False

    print(host)
    print(user["user_id"])

    if user["user_id"] == host:
        return True
    
    return False

def GetEvent(id):
    db, cursor = CreateConnection()

    cursor.execute(f"SELECT * FROM Events WHERE eventID = '{id}'")
    results = cursor.fetchone()
    results = results[:len(results)-3]
    # print(results)
    # name	agelimit	starttime	endtime	desciption	attendee_limit	attendee_no	colour	location	public
    return {
        "name": results[0],
        "agelimit": results[1],
        "start": results[2],
        "end": results[3],
        "description": results[4],
        "attendee_limit": results[5],
        "colour": results[6],
        "location": results[7],
        "public": bool(results[8])
    }

