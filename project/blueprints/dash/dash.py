# DASH MODULE (mounted at root [/dashboard] )

# This is contain a blueprint for 
# - GuestUser Setting Page
# - HostUser Dashboard
# - The View Event Page

from flask import *
from db import accounts as db

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
    if request.method == "POST":
        name = request.form["name"]
        DoB = request.form["DoB"]
        print(name, DoB)

    return render_template("GuestDashboard.html", info=db.getUserInfo(g.user))

@bp.route("/change-password", methods=["POST"])
def ChangePassword():
    new_password = request.form["new-password"]
    old_password = request.form["old-password"]
    print(new_password, old_password, g.user["type"])
    flash("Success! Password has been changed!")
    return redirect(url_for("dash.GuestDashboard"))