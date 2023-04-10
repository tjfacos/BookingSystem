# EVENTS MODULE (mounted at root [/events] )

# This is contain a blueprint for 
# - The Event Details Page
# - The Book Event Page
# - The Create Event Page

from flask import *

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