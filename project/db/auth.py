from werkzeug.security import check_password_hash, generate_password_hash

from db.connection import *
 
UUID = "UUID()"

def AuthoriseUser(email, password):
    """Checks email and password are correct"""
    
    db, cursor = CreateConnection()
    
    cursor.execute(f"SELECT password FROM Accounts WHERE email = '{email}'")
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
    
    account_sql = f"INSERT INTO Accounts (email, password, type, AccountID, user) VALUES ('{info['email']}', '{generate_password_hash(info['password'])}', '{info['type']}', {UUID}, {UUID})" 

    cursor.execute(account_sql)
    db.commit()

    cursor.execute(f"SELECT AccountID, user FROM Accounts where email = '{ info['email'] }'")
    results = cursor.fetchall()
    accountPK = results[0][0]
    userPK = results[0][1]

    if info["type"] == 'host':
        user_sql = "INSERT INTO HostUsers (name, hostID, account) VALUES (%s, %s, %s)"
        val = (info["name"], userPK, accountPK)
    else:
        user_sql = "INSERT INTO GuestUsers (name, DoB, guestID, account, colour) VALUES (%s, %s, %s, %s, %s)"
        val = (info["name"], info["DoB"], userPK, accountPK, "#ffffff")
    
    cursor.execute(user_sql, val)
    db.commit()

    return True


def AccountExists(email: str) -> bool:
    db, cursor = CreateConnection()

    cursor.execute(f"SELECT * FROM Accounts WHERE email='{email}'")
    return bool(cursor.fetchall())

def getUserAccount(email) -> tuple[str, str, str]:
    db, cursor = CreateConnection()
    
    cursor.execute(f"SELECT AccountID, user, type FROM Accounts WHERE email='{email}'")
    return cursor.fetchone()

def ChangePassword(user, old_password, new_password) -> bool:
    db, cursor = CreateConnection()
    
    account_id = user["account_id"]
    cursor.execute(f"SELECT password FROM Accounts WHERE AccountID = '{account_id}'")
    results = cursor.fetchone()

    print(results[0])

    if check_password_hash(results[0], old_password):
        cursor.execute(f"UPDATE Accounts SET password = '{generate_password_hash(new_password)}' WHERE AccountID='{account_id}'")
        db.commit()
        return True
    else:
        return False