# HOME MODULE (mounted at root [/] )

# This is contain a blueprint for 
# - the landing page (/), with the 5 most recent events
# - The search results page

from flask import *

from db import home as db

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
    terms = {}
    search_term = ""
    event_type = ""

    if request.method == "POST":
        print("POST")
        search_term = request.form["search-term"]
        event_type = request.form["type"]

        if search_term:
            terms["search_term"] = search_term
        if event_type:
            terms["type"] = event_type

    # print(terms)

    return render_template("home.html", event_type = event_type, search_term = search_term, events=db.GetHomeContent(**terms))
    

@bp.route("/session")
def getSession():
    return str(g.user)


# tom@example.com: {'account_id': '6d982c82-d7b9-11ed-9fc6-fa79966522e3', 'user_id': '6d982c93-d7b9-11ed-9fc6-fa79966522e3', 'type': 'host'}
# test@test.com: {'account_id': 'aecc752a-d7d4-11ed-9fc6-fa79966522e3', 'user_id': 'aecc7536-d7d4-11ed-9fc6-fa79966522e3', 'type': 'host'}