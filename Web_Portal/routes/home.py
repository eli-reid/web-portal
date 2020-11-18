"""
Routes and views for the flask application.
"""

from .__view_imports import *

@app.context_processor
def inject_data():
    return dict(app=app) 

@app.before_first_request
def initialize():
    #db_init()
    pass

@app.route('/')
def home():
    """Renders the home page."""
    if session.get('username', None):
            return redirect(url_for("user_home", username=session.get('username')))
    return redirect(url_for("login"))

# handle ico request
@app.route("/favicon.ico")
def favicon():
    return ""



