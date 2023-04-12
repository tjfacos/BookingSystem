# DASH MODULE (mounted at root [/dashboard] )

# This is contain a blueprint for 
# - GuestUser Setting Page
# - HostUser Dashboard
# - The View Event Page

from flask import *
from db import accounts as db
from db import auth
from db.events import GetHostEventsList

from blueprints.auth.auth import login_required

bp = Blueprint(
    "dash", 
    __name__, 
    url_prefix="/dashboard",
    template_folder="templates",
    static_folder="static"
)

@bp.route("/guest", methods=["GET", "POST"])
@login_required
def GuestDashboard():
    if g.user["type"] == "host":
        return redirect(url_for("dash.HostDashboard"))
    
    if request.method == "POST":
        name = request.form["name"]
        DoB = request.form["DoB"]
        db.setGuestInfo(g.user, name, DoB)
        flash("Details successfully updated!")
        print("Flashing...")

    tickets = db.GetGuestTickets(g.user)
    print(tickets)

    return render_template(
        "GuestDashboard.html", 
        info=db.getUserInfo(g.user),
        tickets=tickets
        # {
        #     "ticket-id": 5345678945678965456789,
        #     "event-name": "Test Event",
        #     "start-time": "start",
        #     "end-time": "end",
        #     "host-name": "Tom's Venue",
        #     "guest-number": 1,
        #     "guests": "Thomas Facos"
        # }
    )

@bp.route("/change-password", methods=["POST"])
def ChangePassword():
    new_password = request.form["new-password"]
    old_password = request.form["old-password"]
    result = auth.ChangePassword(g.user, old_password, new_password)
    if result:
        flash("Success! Password has been changed!")
    else:
        flash("Sorry! Looks like your old password is incorrect. Please try again.")
    
    return redirect(url_for("dash.GuestDashboard"))

@bp.route("/cancel-ticket", methods=["POST"])
def CancelTicket():
    db.DeleteTicket(request.args.get("ticket"), request.args.get("event"))
    flash("Successfully Deleted Ticket!")
    return redirect(url_for("dash.GuestDashboard"))


@bp.route("/host", methods=["GET", "POST"])
@login_required
def HostDashboard():
    if g.user["type"] == "guest":
        return redirect(url_for("dash.GuestDashboard"))
    
    if request.method == "POST":
        db.setHostInfo(
            g.user, 
            request.form['name'],    
            request.form['colour'],    
            request.form['location'],    
            request.form['description']    
        )
        flash("Details updated successfully!")


    return render_template(
        "HostDashboard.html",
        info=db.getUserInfo(g.user),
        events=GetHostEventsList(g.user)
    )

@bp.route("/delete-account", methods=["GET", "POST"])
def DeleteAccount():
    db.DeleteUser(g.user)
    flash("Successfully Deleted Account")
    return redirect(url_for("auth.sign_out"))