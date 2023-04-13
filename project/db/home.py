from db.connection import *

def GetHostName(id):
    db, cursor = CreateConnection()

    cursor.execute("SELECT name FROM HostUsers WHERE hostID = %s", [id])
    return cursor.fetchone()[0]

def GetHomeContent(**kwargs):
    """Set "search_term" property to perform a search, for words in the title or description of an event. 
    
    Returns 6 most recent events otherwise."""
    
    db, cursor = CreateConnection()

    events = []
    search_term = ""
    type = ""
    
    if kwargs.__contains__("search_term"): search_term = kwargs["search_term"]
    if kwargs.__contains__("type"): type = kwargs["type"]

    if not (search_term or type):
        # There are no set properties, get the 6 most recent, using the created column
        cursor.execute("""
        SELECT name, agelimit, starttime, endtime, colour, location, host, type, eventID, created, attendee_limit, attendee_no
        FROM Events
        WHERE public = true
        ORDER BY created DESC
        """)

        out = cursor.fetchall()
        no = 0
        for result in out:
            if no == 6:
                break
            
            if (result[10] and result[11] >= result[10]):
                continue

            events.append({
                "name": result[0],
                "agelimit": result[1],
                "starttime": result[2],
                "endtime": result[3],
                "colour": result[4],
                "location": result[5],
                "hostID": result[6],
                "host": GetHostName(result[6]),
                "type": result[7],
                "eventID": result[8],
                "created": result[9],
                "attendee_no": result[10]
            })

            no += 1

    
    else:
        if type: # Filter type
            sql = """
            SELECT name, agelimit, starttime, endtime, colour, location, host, type, eventID, attendee_limit, attendee_no
            FROM Events
            WHERE public = true AND type = %s
            ORDER BY created DESC
            """
            values = [type]
        else:
            sql = """
            SELECT name, agelimit, starttime, endtime, colour, location, host, type, eventID, attendee_limit, attendee_no, description
            FROM Events
            WHERE public = true
            ORDER BY created DESC
            """
            values = ()
        
        cursor.execute(sql, values)
        out = cursor.fetchall()

        for result in out:            
            if (result[9] and result[10] >= result[9]):
                continue

            if search_term and result[0].lower().find(search_term.lower()) < 0 and result[-1].lower().find(search_term.lower()) < 0:
                continue


            events.append({
                "name": result[0],
                "agelimit": result[1],
                "starttime": result[2],
                "endtime": result[3],
                "colour": result[4],
                "location": result[5],
                "hostID": result[6],
                "host": GetHostName(result[6]),
                "type": result[7],
                "eventID": result[8],
                "attendee_no": result[9]
            })

            

    return events


def GetHostInfo(id):
    db, cursor = CreateConnection()

    cursor.execute("SELECT name, colour, description FROM HostUsers WHERE hostID=%s", [id])
    results = cursor.fetchone()
    
    info = {
        "name": results[0],
        "colour": results[1],
        "description": results[2]
    }

    cursor.execute("SELECT eventID, name, colour FROM Events WHERE public = true AND host = %s", [id])
    results = cursor.fetchall()
    eventsList = []
    for event in results:
        eventsList.append({
            "eventID": event[0],
            "name": event[1],
            "colour": event[2]
        })

    return info, eventsList
