# EVENTS MODULE (mounted at root [/event] )

# This is contain a blueprint for 
# - The Event Details Page
# - The Book Event Page
# - The Create Event Page

from flask import *
from datetime import date

from blueprints.auth.auth import login_required

from db import events as db
from db.accounts import getUserInfo, DeleteTicket


bp = Blueprint(
    "events", 
    __name__, 
    url_prefix="/event",
    template_folder="templates",
    static_folder="static"
)

@bp.route("/event-details/<event_id>", methods=["GET"])
def EventDetails(event_id):
    return render_template("eventDetails.html", info=db.GetEventDetails(event_id))

@bp.route("book/<event_id>", methods=["GET", "POST"])
@login_required
def BookEvent(event_id):
    if g.user["type"] == "host":
        flash("A guest account is required to book tickets")
        return redirect(url_for("dash.HostDashboard"))
    
    info = db.GetEventDetails(event_id)
    user = getUserInfo(g.user)

    user["age"] = ageInYears(user["DoB"])

    if user["age"] < info["agelimit"]:
        flash(f"Sorry! The age limit for this event is {info['agelimit']}")
        return redirect(url_for("dash.GuestDashboard"))


    if request.method == "POST":
        names = []
        for field in request.form:
            if "name" in field:
                names.append(request.form[field])
        
        db.CreateTicket(event_id, g.user, ', '.join(names))
        flash("Success! Your Tickets have been booked!")
        return redirect(url_for("dash.GuestDashboard"))

    return render_template("bookEvent.html", info=info, user=user)

def ageInYears(birthDate):

    today = date.today()
    lastYearBirthday = date(today.year - 1, birthDate.month, birthDate.day)
    currYearBirthday = date(today.year, birthDate.month, birthDate.day)


    if currYearBirthday > today:
        years = lastYearBirthday.year - birthDate.year
    else:
        years = currYearBirthday.year - birthDate.year

    return years


@bp.route("/create-event")
@login_required
def CreateEvent():
    id = db.CreateEvent(g.user)
    return redirect(url_for("events.EditEvent", event_id=id))

@bp.route("/viewGuests/<event_id>")
@login_required
def ViewGuests(event_id):

    if not db.EventBelongsToUser(event_id, g.user):
        return redirect(url_for("home.home"))
    
    info, guestList = db.GetGuestList(event_id)
    info["eventID"] = event_id

    return render_template("viewGuests.html", info=info, guestList=guestList)





@bp.route("/deleteGuest", methods = ["POST"])
@login_required
def DeleteGuest():
    
    # print(request.args.get("ticket"))
    # print(request.args.get("event"))

    DeleteTicket(request.args.get("ticket"), request.args.get("event"))

    flash("Success! Guest has been deleted.")

    return redirect(url_for("events.ViewGuests", event_id=request.args.get("event")))


@bp.route("/edit-event/<event_id>", methods=["GET", "POST"])
@login_required
def EditEvent(event_id):
    if not db.EventBelongsToUser(event_id, g.user):
        return redirect(url_for("home.home"))    
        

    if request.method == "POST":
        info = {}
        public = False
        for item in request.form:
            info[item] = request.form[item]
            match item:
                case "agelimit":
                    info[item] = int(info[item])
                case "attendee_limit":
                    if request.form[item]:
                        info[item] = int(info[item])
                    else:
                        info[item] = -1
                case "starttime" | "endtime":
                    info[item] = info[item].replace("T", " ")
                case "public":
                    public = True

        info["public"] = public

        info["eventID"] = event_id
        # print(info)
        db.UpdateEvent(info)
        flash("Updated Successfully!")


    return render_template("editEvent.html", info = db.GetEvent(event_id), event_id = event_id)
    # name	agelimit	starttime	endtime	desciption	attendee_limit	attendee_no	colour	location	public
    
@bp.route("/cancel/<id>", methods=["POST"])
def CancelEvent(id):
    db.CancelEvent(id)
    flash("Event sucessfully deleted!!!")
    return redirect(url_for("dash.HostDashboard"))