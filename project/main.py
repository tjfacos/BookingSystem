from flask import Flask, request, jsonify
# from db import *

app = Flask(__name__)

@app.route("/")
def root():
    return "Hello, Flask!"

@app.route("/auth", methods=["POST"])
def authUser():
    credentials = request.get_json()
    user = credentials["user"]
    pwd = credentials["pwd"]
    print(user)
    print(pwd)
    return "0"

def main():
    app.run(host="0.0.0.0", port=5000)

main()