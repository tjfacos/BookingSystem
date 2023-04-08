from dotenv import load_dotenv
import os
import mysql.connector


load_dotenv()

UUID = "UNHEX(REPLACE(UUID(), '-', ''))"

def InsertUser(info : dict) -> bool:
    db = mysql.connector.connect(
        host= os.getenv("HOST"),
        user=os.getenv("USER"),
        passwd= os.getenv("PASSWORD"),
        ssl_verify_identity=True,
        ssl_ca="cacert.pem"
    )

    cursor = db.cursor()
    
    """

    Info must always include
    - email
    - password
    - type
    - name
    
    If user is a guest, info must also include
    - DoB
    """
    
    
    account_sql = "INSERT INTO Accounts (email, password, type, AccountID, user) VALUES (%s, %s, %s, " + UUID + ", " + UUID + ")" # email, password, type 

    cursor.execute(account_sql, (
        info["email"],
        info["password"],
        info["type"],
    ))

    db.commit()

    cursor.execute(f"SELECT AccountID, user FROM Accounts where email = '{ info['email'] }'")
    results = cursor.fetchall()
    accountPK = results[0][0]
    userPK = results[0][1]

    if info["type"] == 'host':
        user_sql = "INSERT INTO HostUsers (name, hostID, account) VALUES (%s, %s, %s)"
        val = (info["name"], userPK, accountPK)
    else:
        user_sql = "INSERT INTO GuestUsers (name, DoB, guestID, account) VALUES (%s, %s, %s, %s)"
        val = (info["name"], info["DoB"], userPK, accountPK)
    
    cursor.execute(user_sql, val)
    db.commit()

    return True


def AccountExists(email: str) -> bool:

    db = mysql.connector.connect(
        host= os.getenv("HOST"),
        user=os.getenv("USER"),
        passwd= os.getenv("PASSWORD"),
        ssl_verify_identity=True,
        ssl_ca="cacert.pem"
    )

    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM Accounts WHERE email='{email}'")
    return bool(cursor.fetchall())
