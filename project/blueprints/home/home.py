# HOME MODULE (mounted at root [/] )

# This is contain a blueprint for 
# - the landing page (/), with the 5 most recent events
# - The search results page

from flask import *

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

    return render_template("home.html", events=[{
        "name": "Test Event",
        "id": 1234567
    }])
    

@bp.route("/session")
def getSession():
    return str(g.user)


# tom@example.com: {'account_id': '6d982c82-d7b9-11ed-9fc6-fa79966522e3', 'user_id': '6d982c93-d7b9-11ed-9fc6-fa79966522e3', 'type': 'host'}
# test@test.com: {'account_id': 'aecc752a-d7d4-11ed-9fc6-fa79966522e3', 'user_id': 'aecc7536-d7d4-11ed-9fc6-fa79966522e3', 'type': 'host'}