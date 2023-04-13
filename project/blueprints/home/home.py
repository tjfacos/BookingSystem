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


    return render_template("home.html", event_type = event_type, search_term = search_term, events=db.GetHomeContent(**terms))
    

@bp.route("/session")
def getSession():
    return str(g.user)



@bp.route("/view-host/<host_id>", methods=["GET"])
def ViewHost(host_id):
    info, events = db.GetHostInfo(host_id)
    return render_template("viewHost.html", info=info, events=events)