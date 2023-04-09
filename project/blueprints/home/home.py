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
    return "Hello, home!"