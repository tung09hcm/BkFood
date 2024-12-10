from flask import Blueprint, render_template, request, flash  # type: ignore

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')

        if len(email) < 4:
            flash("Invalid email", category = 'error')
        elif len(username) < 2:
            flash("Username must be greater than 2 characters", category = 'error')
        elif password != confirm_password:
            flash("Passwords don\'t match", category = 'error')
        elif len(password) < 7:
            flash("Passwords must be greater than 7 characters", category = 'error')
        else:
            # add user to database
            flash("Account created!", category = 'success')

    return render_template("register.html")

