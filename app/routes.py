
from flask import request, make_response, send_file, session
from flask.ext.login import (LoginManager, login_user, logout_user, 
                            current_user, login_required, confirm_login)
import uuid

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
@login_required
def create_group():

    group_id = None

    try:
        user_id = current_user.get_id()
        group_name = request.form["group_name"]

        if(len(group_name.strip()) == 0):
            return "Group name is blank"

        groupDAO = GroupDAO()
        group_id = groupDAO.add(group_name, user_id)

    except Exception as e:
        print "error reading form data"
        print e

    return group_id.__str__()

@app.route("/group", methods=["GET"])
@login_required
def get_user_groups():

    group_id = None
    groups = None

    try:
        user_id = current_user.get_id()

        groupDAO = GroupDAO()
        groups = groupDAO.get_all(user_id)

    except Exception as e:
        print "routes - get all groups"
        print e

    result = [g.__str__() for g in groups]
    print result
    return str(result)

