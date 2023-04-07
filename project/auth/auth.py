# AUTH MODULE

from flask import *
from werkzeug.security import check_password_hash, generate_password_hash

import functools

bp = Blueprint(
    "auth", 
    __name__, 
    url_prefix="/auth",
    template_folder="templates"
)

def authorise(email, password):
    print(email, password)

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


@bp.route("/register")
def register():
    return render_template("register.html")