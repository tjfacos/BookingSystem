from db.connection import *

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
        sql = "DELETE FROM HostUsers WHERE hostID = %s"
    else:
        sql = "DELETE FROM GuestUsers WHERE guestID = %s"

    cursor.execute(sql, [user_id])
    cursor.execute("DELETE FROM Accounts WHERE AccountID = %s", [account_id])

    db.commit()
