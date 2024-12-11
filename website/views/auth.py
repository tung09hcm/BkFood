from flask import Blueprint, render_template, request, flash, session, redirect, url_for  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from website.controllers.usercontroller import UserController

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if "user" in session:
        user = session["user"]
        return redirect(url_for('views.home', usr = user))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserController()
        response = user.login(email,password)
        if response == None:
            flash("Wrong username or password", category = 'error')
        else:
            session["user"] = response[0]
            return redirect(url_for('views.home', usr = response[0]))
    return render_template("login.html")

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if "user" in session:
        user = session["user"]
        return redirect(url_for('views.home', usr = user))
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
        elif int(age) <= 0:
            flash("Invalid age", category = 'error')
        elif int(height) <= 100 or int(height) > 250:
            flash("Invalid height", category = 'error')
        elif int(weight) <= 10:
            flash("Invalid weight", category = 'error')
        else:
            # add user to database
            user = UserController()
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
               
            response = user.add_user(username,email,password_hash,age,gender,height,weight)
            print("response_at_auth_register: ")
            print(response[0]['id'])
            flash("Account created!", category = 'success')
            session["user"] = response[0]
            return redirect(url_for('views.home', usr = response[0]))


    return render_template("register.html")

@auth.route('/logout')
def logout():
    # Xóa toàn bộ dữ liệu trong session
    session.clear()
    return redirect(url_for('auth.login'))