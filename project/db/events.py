from db.connection import *
from db.home import GetHostName
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

    cursor.execute("SELECT name, agelimit, starttime, endtime, description, attendee_limit, colour, location, public, type FROM Events WHERE eventID = %s", [id])
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
        "public": bool(results[8]),
        "type": results[9]
    }

    # print(info)
    return info

def GetHostEventsList(user) -> list[dict]:
    db, cursor = CreateConnection()
    
    hostID = user["user_id"]

    cursor.execute(
        "SELECT name, agelimit, starttime, endtime, description, attendee_limit, attendee_no, colour, location, public, eventID, type FROM Events WHERE host = %s", 
        [
            hostID
        ]
    )

    results = cursor.fetchall()
    print(results)
    events = []
    for result in results:
        events.append({
            "name": result[0],
            "agelimit": result[1],
            "starttime": result[2],
            "endtime": result[3],
            "description": result[4],
            "attendee_limit": result[5],
            "attendee_no": result[6],
            "colour": result[7],
            "location": result[8],
            "public": bool(result[9]),
            "eventID": result[10],
            "type": result[11]
        })
    
    return events







def UpdateEvent(info : dict):
    db, cursor = CreateConnection()
    if info["attendee_limit"] < 0:
        info["attendee_limit"] = None
    
    sql = """
    UPDATE Events 
    SET name = %s, agelimit = %s, starttime = %s, endtime=%s,
    description = %s, attendee_limit = %s, colour = %s, 
    location = %s, type = %s, public = %s WHERE eventID = %s
    """

    values = list(info.values())
    
    cursor.execute(sql, values)
    db.commit()


def GetEventDetails(id):
    db, cursor = CreateConnection()
    sql = """
            SELECT name, agelimit, starttime, endtime, colour, location, host, type, eventID, attendee_limit, attendee_no, description, public
            FROM Events
            WHERE eventID = %s
        """
    cursor.execute(sql, [id])
    result = cursor.fetchone()    
    
    info = {
        "name": result[0],
        "agelimit": result[1],
        "starttime": result[2],
        "endtime": result[3],
        "colour": result[4],
        "location": result[5],
        "host": GetHostName(result[6]),
        "type": result[7],
        "eventID": result[8],
        "description": result[11],
        "public": bool(result[12])
    }
    
    if result[9]:
        info["place_left"] =  result[9]-result[10]

    return info

def CreateTicket(eventID: str, user, names: str):
    sql = """
    INSERT INTO Tickets
    VALUES (UUID(), %s, %s, %s)
    """
    values = (user["user_id"] ,eventID, names)

    db, cursor = CreateConnection()
    cursor.execute(sql, values)
    db.commit()