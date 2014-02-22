
from flask import request, make_response, send_file, session
from flask.ext.login import (LoginManager, login_user, logout_user, 
                            current_user, login_required, confirm_login)

from app import app
from DAO.userDAO import UserDAO
from DAO.groupDAO import GroupDAO
from DAO.postDAO import PostDAO
from model.user import User
from model.group import Group
from model.post import Post

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    user = UserDAO(app.secret_key)
    return user.get(id)


# display index.html
@app.route("/")
def index():
    return send_file("static/index.html")


# login the user
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    if email and password:
        user_mapper = UserDAO(app.secret_key)
        user = user_mapper.validate(email, password)
        
        if user:
            #login user
            login_user(user)
            return "user logged in"

        else:
            return "wrong user / password"

    else:
        return "email / password not supplied"


# logout user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "user logged out"


# create a group
@app.route("/group", methods=["POST"])
def create_group():
    
    # check if user is logged in
    if "user" not in session:
        return "user not logged in"

    group = Group()
    group_name = None

    try:
        group_name = request.form["group_name"]

        if(len(group_name.strip()) == 0):
            return "Group name is blank"

        groupDAO = GroupDAO()
        groupDAO.add_group(group_name)

    except Exception as e:
        print "error reading form data"
        print e

    group.name = group_name

