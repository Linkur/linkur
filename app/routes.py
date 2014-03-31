
from flask import request, make_response, send_file, session
from flask.ext.login import (LoginManager, login_user, logout_user, 
        current_user, login_required, confirm_login)
from datetime import datetime

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
    user = UserDAO()
    return user.get(id)


# display index.html
@app.route("/")
def index():
    return send_file("static/index.html")


# user signup
@app.route("/signup", methods=["POST"])
def signup():

    email = request.form["email"]
    uname = request.form["name"]
    password = request.form["password"]
    repeat = request.form["repeat"]

    result = None

    try:
        if email and uname and password and repeat:

            email = email.lower()
            uname = uname.strip()

            user = User()
            user.name = uname
            user.email = email
            user.password = password

            user_mapper = UserDAO()
            result = user_mapper.add(user)

        else:
            return "params error"

    except Exception as e:
        print "error while signing up user"
        print e

    return result


# login the user
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]
    print password

    if email and password:
        email = email.lower()
        user_mapper = UserDAO()
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

    if groups:
        result = [g.__str__() for g in groups]
        print result

    return str(result)


@app.route("/post", methods=["POST"])
@login_required
def create_post():

    post = Post()
    user_id = current_user.get_id()
    result = None

    try:
        post.title = request.form["title"]
        post.link = request.form["link"]
        post.group = request.form["group"]
        tags = request.form["tags"]
        print tags
        post.tags = []

        if tags:
            tags = tags.split(",")
            # convert tags to list
            for word in tags:
                stripped = word.strip()

                if len(stripped) > 0:
                    post.tags.append(stripped)

        print post.tags
        print type(post.tags)
        post.added_by = user_id
        post.date = datetime.utcnow()

        post_mapper = PostDAO()
        result = post_mapper.create(post)

    except Exception as e:

       print "error while creating post"
       print e

    return str(result)


@app.route("/post/<post_id>", methods=["GET"])
@login_required
def get_post(post_id):

    post = Post()
    user_id = current_user.get_id()
    result = None

    if post_id:

        try:

            post_mapper = PostDAO()
            result = post_mapper.get(post_id)

        except Exception as e:

            print "Error getting specific post"
            print e

    else:

        result = "post_id empty"

    return str(result.__str__())


