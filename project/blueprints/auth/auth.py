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
    session["account_id"], session["user_id"], session["type"] = db.getUserAccount(email)
    print(session["account_id"])
    print(session["user_id"])
    print(session["type"])


def authorise(email, password):
    if db.AuthoriseUser(email, password):
        print("Sign in sucessfull!")
        return True
    else:
        flash("Sorry! Invalid email or password. Please try again.")
        return False

def registerNewUser(**properties): 

    if db.AccountExists(properties["email"]):
        flash("Sorry! An account for this email already exists!")
        return render_template("register.html")


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

    return redirect(url_for("home.home"))



@bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if authorise(
            email, 
            password
        ):
            # print("Attempting redirect...")
            
            CreateNewSession(email)   
            
            return redirect(url_for("home.home"))


    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["type"] == "host":
            
            return registerNewUser(
                email = request.form["email"],
                password = request.form["password"],
                name = request.form["name"],
                type = request.form["type"]
            )
        
        else:
            return registerNewUser(
                email = request.form["email"],
                password = request.form["password"],
                name = request.form["name"],
                type = request.form["type"],
                DoB = request.form["DoB"]
            )

    return render_template("register.html")