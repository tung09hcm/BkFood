from flask import Blueprint, render_template, session, redirect, url_for  # type: ignore

views = Blueprint('views', __name__)


@views.route('/')
def home():
    if "user" in session:
        user = session["user"]
        return render_template("home.html")
    else: 
        return redirect(url_for('auth.login'))
    
    