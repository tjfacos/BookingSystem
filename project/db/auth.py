from werkzeug.security import check_password_hash, generate_password_hash

from db.connection import *

def AuthoriseUser(email, password):
    """Checks email and password are correct"""
    
    db, cursor = CreateConnection()
    
    cursor.execute("SELECT password FROM Accounts WHERE email = %s", [email] )
    results = cursor.fetchone()
    
    if not results:
        return False
    
    return check_password_hash(results[0], password)


def InsertUser(info : dict) -> bool:
    """

    Info must always include
    - email
    - password
    - type
    - name
    
    If user is a guest, info must also include
    - DoB
    """
    
    db, cursor = CreateConnection()
    
    account_sql = "INSERT INTO Accounts (email, password, type, AccountID, user) VALUES (%s, %s, %s, UUID(), UUID())" 
    cursor.execute(account_sql, (
        info["email"],
        generate_password_hash(info["password"]),
        info["type"]
    ))

    db.commit()

    cursor.execute("SELECT AccountID, user FROM Accounts where email = %s", [ info["email"] ])
    results = cursor.fetchall()
    accountPK = results[0][0]
    userPK = results[0][1]

    if info["type"] == 'host':
        user_sql = "INSERT INTO HostUsers (name, hostID, account, colour, location, description) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (info["name"], userPK, accountPK, "#ffffff", "", "")
    else:
        user_sql = "INSERT INTO GuestUsers (name, DoB, guestID, account) VALUES (%s, %s, %s, %s)"
        val = (info["name"], info["DoB"], userPK, accountPK)
    
    cursor.execute(user_sql, val)
    db.commit()

    return True


def AccountExists(email: str) -> bool:
    db, cursor = CreateConnection()

    cursor.execute("SELECT * FROM Accounts WHERE email=%s", [email])
    return bool(cursor.fetchall())

def getUserAccount(email) -> tuple[str, str, str]:
    db, cursor = CreateConnection()
    
    cursor.execute("SELECT AccountID, user, type FROM Accounts WHERE email=%s", [email])
    return cursor.fetchone()

def ChangePassword(user, old_password, new_password) -> bool:
    db, cursor = CreateConnection()
    
    account_id = user["account_id"]
    cursor.execute("SELECT password FROM Accounts WHERE AccountID = %s", [account_id])
    results = cursor.fetchone()

    if check_password_hash(results[0], old_password):
        cursor.execute("UPDATE Accounts SET password = %s WHERE AccountID=%s", (
            generate_password_hash(new_password),
            account_id
        ))
        db.commit()
        return True
    else:
        return False