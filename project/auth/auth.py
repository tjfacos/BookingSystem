# AUTH MODULE

from flask import *
from werkzeug.security import check_password_hash, generate_password_hash

import functools

bp = Blueprint(
    "auth", 
    __name__, 
    url_prefix="/auth",
    template_folder="templates",
    static_folder="static"
)

def authorise(email, password):
    print(email, password)

def registerNewUser(email, password): 

    # Function to check
    # - Check user doesn't already exist (check email not already registered, and alert user if so)
    # - If user doesn't exist, insert details into database (securely)
    # - Redirect user to their account page / dashboard

    pass

@bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        authorise(
            email, 
            password
        )

    # print("Flashing...")
    # flash("Test")

    return render_template("login.html")


@bp.route("/register")
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        registerNewUser(
            email, 
            password
        )

    return render_template("register.html")