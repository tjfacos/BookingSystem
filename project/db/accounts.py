from db.connection import *

def getUserInfo(user):
    db, cursor = CreateConnection()
    user_id = user["user_id"]
    
    if user["type"] == "host":
        cursor.execute(f"SELECT name, description, location, colour FROM HostUsers WHERE hostID = '{user_id}' ")
        result = cursor.fetchone()
        return {
            "name": result[0],
            "description": result[1],
            "location": result[2],
            "colour": result[3]
        }
    
    else:
        cursor.execute(f"SELECT name, DoB FROM GuestUsers WHERE guestID = '{user_id}' ")
        result = cursor.fetchone()
        return {
            "name": result[0],
            "DoB": result[1]
        }
    
def setGuestInfo(user, name, DoB):
    db, cursor = CreateConnection()
    user_id = user["user_id"]

    cursor.execute(f"UPDATE GuestUsers SET name = '{name}', DoB = '{DoB}' WHERE GuestID='{user_id}'")
    db.commit()