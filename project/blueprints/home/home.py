# HOME MODULE (mounted at root [/] )

# This is contain a blueprint for 
# - the landing page (/), with the 5 most recent events
# - The search results page

from flask import *
from db import auth

import functools

bp = Blueprint(
    "home", 
    __name__, 
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="home/static"
)

@bp.route("/")
def home():
    return render_template("home.html")
    