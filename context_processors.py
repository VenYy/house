from flask import g, session


def inject_user():
    if 'username' in session:
        g.current_user = session['username']
    else:
        g.current_user = None
