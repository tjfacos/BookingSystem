# AUTH MODULE

from flask import *
from db import db

import functools

bp = Blueprint(
    "auth", 
    __name__, 
    url_prefix="/auth",
    template_folder="templates",
    static_folder="static"
)

def CreateNewSession(email):
    session.clear()
    session["account_id"], session["user_id"], session["type"] = db.getUserAccount()
    return redirect(url_for("home"))


def authorise(email, password):
    if db.AuthoriseUser(email, password):
        flash("Sign-in Successful!")
        CreateNewSession(email)
    else:
        flash("Sorry! Invalid email or password. Please try again.")

def registerNewUser(**properties): 

    # Function to check
    # - Check user doesn't already exist (check email not already registered, and alert user if so)
    # - If user doesn't exist, insert details into database (securely)
    # - Redirect user to their account page / dashboard
    
    if db.AccountExists(properties["email"]):
        flash("Sorry! An account for this email already exists!")
        return


    info = {
        "email": properties["email"],
        "password": properties["password"],
        "type": properties["type"],
        "name": properties["name"]
    }

    if info["type"] == "guest":
        info["DoB"] = properties["DoB"]

    db.InsertUser(info)

    CreateNewSession(properties["email"])

    

@bp.route("/sign-in", methods=["GET", "POST"])

def sign_in():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        authorise(
            email, 
            password
        )


    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    # print("Register Request")
    if request.method == "POST":
        # print("POST!!!!!")
        if request.form["type"] == "host":
            # print("Registering host...")
            
            registerNewUser(
                email = request.form["email"],
                password = request.form["password"],
                name = request.form["name"],
                type = request.form["type"]
            )
        
        else:
            # print("Registering guest...")

            registerNewUser(
                email = request.form["email"],
                password = request.form["password"],
                name = request.form["name"],
                type = request.form["type"],
                DoB = request.form["DoB"]
            )

    return render_template("register.html")