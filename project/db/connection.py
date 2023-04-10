from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

UUID = "UUID()"

def CreateConnection():
    db = mysql.connector.connect(
        host= os.getenv("HOST"),
        user=os.getenv("USER"),
        passwd= os.getenv("PASSWORD"),
        ssl_verify_identity=True,
        ssl_ca="cacert.pem"
    )

    cursor = db.cursor()

    return db, cursor