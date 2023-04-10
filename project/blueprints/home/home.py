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

@bp.route("/", methods=["GET", "POST"])
def home():
    search_term = request.args.get("search-term")
    if search_term:
        flash(f"No events found for '{ search_term }'")
    else:
        flash("No events found.")

    return render_template("home.html")
    