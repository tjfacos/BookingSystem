from db.connection import *
from db.home import GetHostName


def getUserInfo(user):
    db, cursor = CreateConnection()
    user_id = user["user_id"]
    
    if user["type"] == "host":
        cursor.execute("SELECT name, description, location, colour FROM HostUsers WHERE hostID = %s", [ user_id ])
        result = cursor.fetchone()
        return {
            "name": result[0],
            "description": result[1],
            "location": result[2],
            "colour": result[3]
        }
    
    else:
        cursor.execute("SELECT name, DoB FROM GuestUsers WHERE guestID = %s", [user_id] )
        result = cursor.fetchone()
        return {
            "name": result[0],
            "DoB": result[1]
        }
    
def setGuestInfo(user, name, DoB):
    db, cursor = CreateConnection()
    user_id = user["user_id"]

    cursor.execute("UPDATE GuestUsers SET name = %s, DoB = %s WHERE guestID=%s", (
        name,
        DoB,
        user_id
    ))

    db.commit()

def setHostInfo(user, name, colour, location, description):
    db, cursor = CreateConnection()
    user_id = user["user_id"]
    
    
    cursor.execute("UPDATE HostUsers SET name = %s, colour = %s, location = %s, description = %s WHERE hostID=%s", (
        name,
        colour,
        location,
        description,
        user_id
    ))
    db.commit()

def DeleteUser(user):
    db, cursor = CreateConnection()
    user_id = user["user_id"]
    account_id = user["account_id"]
    type = user["type"]

    if type == "host":
        cursor.execute("""DELETE FROM HostUsers WHERE hostID = %s; """, [user_id])
        cursor.execute("DELETE FROM Tickets WHERE event IN (SELECT eventID FROM Events WHERE host = %s)", [user_id], multi=True); 
        cursor.execute("""DELETE FROM Events WHERE host = %s""", [user_id])
    else:
        cursor.execute("DELETE FROM GuestUsers WHERE guestID = %s", [user_id])

    cursor.execute("DELETE FROM Accounts WHERE AccountID = %s", [account_id])

    db.commit()









def GetGuestTickets(user):
    db, cursor = CreateConnection()
    user_id = user["user_id"]

    events = []

    sql = "SELECT ticketID, event, guestName FROM Tickets WHERE purchaser = %s"
    cursor.execute(sql, [user_id])
    results = cursor.fetchall()
    
    for result in results:
        cursor.execute(
            """
            SELECT name, starttime, endtime, colour, location, host, type
            FROM Events
            WHERE eventID = %s
            """, [ result[1] ]
        )
        event = cursor.fetchone()

        events.append({
            "ticketID": result[0],
            "eventID": result[1],
            "guestName": result[2],
            "name": event[0],
            "starttime": event[1],
            "endtime": event[2],
            "colour": event[3],
            "location": event[4],
            "host": GetHostName(event[5]),
            "type": event[6]
        })

    return events

def DeleteTicket(ticket, event):
    # print("DELETEING TICKET")
    # print(ticket, event)
    
    db, cursor = CreateConnection()
    
    cursor.execute("DELETE FROM Tickets WHERE ticketID = %s", [ticket])
    cursor.execute("UPDATE Events SET attendee_no = attendee_no - 1 WHERE eventID = %s", [event])

    db.commit()