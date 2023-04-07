from dotenv import load_dotenv
import os
import mysql.connector


load_dotenv()

print(os.getenv("HOST"))
print(os.getenv("USERNAME"))
print(os.getenv("PASSWORD"))


db = mysql.connector.connect(
    host= os.getenv("HOST"),
    user=os.getenv("USERNAME"),
    passwd= os.getenv("PASSWORD"),
    ssl_verify_identity=True,
    ssl_ca="cacert.pem"
)

cursor = db.cursor()

def test():
    statement = "INSERT INTO Events (name, host, attendee_no) values (%s, %s, %s)"
    val = ("localEvent", 7, 13)

    cursor.execute(statement, val)

    db.commit()