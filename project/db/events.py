from db.connection import *
from datetime import datetime

def CreateEvent(user):
    db, cursor = CreateConnection()

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT COUNT(*) FROM Events WHERE host = %s", [ user["user_id"] ])
    name = f"My Event {cursor.fetchone()[0]}"

    cursor.execute("INSERT INTO Events (eventID, attendee_no, host, public, name, created) VALUES (UUID(), %s, %s, %s, %s, %s)", (
        0,
        user["user_id"],
        False,
        name,
        time
    ))

    db.commit()

    cursor.execute("SELECT eventID FROM Events WHERE created = %s", [time])
    id = cursor.fetchone()[0]

    return id








def EventBelongsToUser(id, user):
    db, cursor = CreateConnection()

    cursor.execute("SELECT host FROM Events WHERE eventID = %s", [id])
    try:
        host = cursor.fetchone()[0]
    except TypeError:
        return False


    if user["user_id"] == host:
        return True
    
    return False

def GetEvent(id):
    db, cursor = CreateConnection()

    cursor.execute("SELECT name, agelimit, starttime, endtime, description, attendee_limit, colour, location, public FROM Events WHERE eventID = %s", [id])
    results = cursor.fetchone()
    # name	agelimit	starttime	endtime	desciption	attendee_limit	attendee_no	colour	location	public
    info = {
        "name": results[0],
        "agelimit": results[1],
        "starttime": results[2],
        "endtime": results[3],
        "description": results[4],
        "attendee_limit": results[5],
        "colour": results[6],
        "location": results[7],
        "public": bool(results[8])
    }

    print(info)
    return info

def UpdateEvent(info : dict):
    db, cursor = CreateConnection()
    sql = """
    UPDATE Events 
    SET name = %s, agelimit = %s, starttime = %s, endtime=%s,
    description = %s, attendee_limit = %s, colour = %s, 
    location = %s, public = %s WHERE eventID = %s
    """

    values = list(info.values())
    
    cursor.execute(sql, values)
    db.commit()
