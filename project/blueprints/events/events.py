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

@bp.route("/edit-event/<event_id>")
@login_required
def EditEvent(event_id):
    print(g.user)
    if not db.EventBelongsToUser(event_id, g.user):
        print("Naughty...")
        return redirect(url_for("home.home"))    
        
    return render_template("editEvent.html")