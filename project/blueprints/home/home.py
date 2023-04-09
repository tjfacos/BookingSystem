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
    static_folder="static"
)

@bp.route("/")
def home():
    if g.user:
        return str(g.user)
    
    return "Hello, home!"
    