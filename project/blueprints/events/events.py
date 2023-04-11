# EVENTS MODULE (mounted at root [/events] )

# This is contain a blueprint for 
# - The Event Details Page
# - The Book Event Page
# - The Create Event Page

from flask import *
from blueprints.auth.auth import login_required

from db import events as db

bp = Blueprint(
    "events", 
    __name__, 
    url_prefix="/event",
    template_folder="templates",
    static_folder="static"
)

@bp.route("/event-details/<event_id>")
def eventDetails(event_id):
    return event_id

@bp.route("/create-event")
@login_required
def CreateEvent():
    id = db.CreateEvent(g.user)
    return redirect(url_for("events.EditEvent", event_id=id))

@bp.route("/edit-event/<event_id>", methods=["GET", "POST"])
@login_required
def EditEvent(event_id):
    # print(g.user)
    if not db.EventBelongsToUser(event_id, g.user):
        print("Naughty...")
        return redirect(url_for("home.home"))    
        

    if request.method == "POST":
        # print(request.form)
        info = {}
        public = False
        for item in request.form:
            print(item)
            info[item] = request.form[item]
            match item:
                case "agelimit" | "attendee_limit":
                    info[item] = int(info[item])
                case "starttime" | "endtime":
                    info[item] = info[item].replace("T", " ")
                case "public":
                    public = True

        info["public"] = public

        info["eventID"] = event_id
        print(info)
        db.UpdateEvent(info)
        flash("Updated Successfully!")



    return render_template("editEvent.html", info = db.GetEvent(event_id))
    # name	agelimit	starttime	endtime	desciption	attendee_limit	attendee_no	colour	location	public
    