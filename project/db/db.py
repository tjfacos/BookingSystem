from dotenv import load_dotenv
import os
import mysql.connector


load_dotenv()



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
    
    
    account_sql = "INSERT INTO Accounts (email, password, type) VALUES (%s, %s, %s)" # email, password, type 
    # NB: Account must be created before user, then set user using account PK, then add user onto account

    cursor.execute(account_sql, (
        info["email"],
        info["password"],
        info["type"]
    ))

    db.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    accountPK = cursor.fetchall()[0][0]

    if info["type"] == 'host':
        user_sql = "INSERT INTO HostUsers (name, account) VALUES (%s, %s)"
        val = (info["name"], accountPK)
    else:
        user_sql = "INSERT INTO GuestUsers (name, account, DoB) VALUES (%s, %s, %s)"
        val = (info["name"], accountPK, info["DoB"])
    
    cursor.execute(user_sql, val)
    db.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    userPK = cursor.fetchall()[0][0]

    cursor.execute(f"UPDATE Accounts SET user = {userPK} where AccountID = {accountPK}")
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
