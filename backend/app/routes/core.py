from datetime import timedelta
from flask import current_app as app, session


@app.before_request
def make_session_permanent():
    session.permanent = False
    session.permanent_session_lifetime = timedelta(days=7)
