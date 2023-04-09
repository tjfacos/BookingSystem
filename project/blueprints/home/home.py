# HOME MODULE (mounted at root [/] )

from flask import *
from db import db

import functools

bp = Blueprint(
    "home", 
    __name__, 
    url_prefix="/",
    template_folder="templates",
    static_folder="static"
)

@bp.route("/")
def home():
    print(session["account_id"])
    print(session["user_id"])
    print(session["type"])
    return "Hello, home!"
    