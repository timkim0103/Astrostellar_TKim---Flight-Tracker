from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.craft import Craft
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    #users = User.get_all()
    return render_template('index.html')

@app.route('/register',methods=['POST']) # To get to the create new user page
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    passwordhash = bcrypt.generate_password_hash(request.form['password']) # Store bcrypt into variable
    data ={ 
        "firstname": request.form['firstname'],
        "lastname": request.form['lastname'],
        "email": request.form['email'],
        "password": passwordhash # utilize a salt and hash
    }
    id = User.save(data)
    if not id:
        flash("Email is already taken.", "register")
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST']) # To get to the login page for an existing user
def login():
    data = {
        "email": request.form["email"]
    }
    user = User.get_by_email(data)


    if not user:
        flash("Invalid Email or Password","login")
        # print("**********************************")
        # print(user.password)
        return redirect('/')
    elif not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email or Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/crafts')

@app.route('/dashboard') # To return to the dashboard
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    # user = User.get_one(data)
    # songs = Song.get_songs(data)
    # users = User.get_all()
    # print(messages[0])
    return render_template("dashboard.html",user=User.get_one(data))

@app.route('/logout') # Log out
def logout():
    session.clear()
    return redirect('/')


# @app.route('/success')
# def success():
#     data = {
#         "id": session['user_id']
#     }
#     return render_template('dashboard.html', user = User.get_by_id(data))