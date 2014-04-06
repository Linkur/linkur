
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
from app.utils.jsonWrapper import JsonWrapper

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
            return JsonWrapper.get_json(True, "params error")

    except Exception as e:
        print "error while signing up user"
        print e

    if result:
        return JsonWrapper.get_json(False)
    else:
        return JsonWrapper.get_json(True, "Error signing up user")


# login the user
@app.route("/login", methods=["POST"])
def login():

    result = None
    email = request.form["email"]
    password = request.form["password"]

    if email and password:
        email = email.lower()
        user_mapper = UserDAO()
        user = user_mapper.validate(email, password)

        if user:
            #login user
            is_success = login_user(user)
            if is_success:
                result = JsonWrapper.get_json(False, "User logged in")
            else:
                result = JsonWrapper.get_json(True, "Check user/password")

        else:
            result = JsonWrapper.get_json(True, "Check user/password")

    else:
        result = JsonWrapper.get_json(True, "email / password not supplied")

    return result


# logout user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return JsonWrapper.get_json(False, "User logged out")


# create a group
@app.route("/group", methods=["POST"])
@login_required
def create_group():

    group_id = None
    result = None

    try:
        user_id = current_user.get_id()
        group_name = request.form["group_name"]

        if(len(group_name.strip()) == 0):
            return "Group name is blank"

        groupDAO = GroupDAO()
        group_id = groupDAO.add(group_name, user_id)

        if group_id:
            result = JsonWrapper.get_json(False, group_id)

        else:
            result = JsonWrapper.get_json(True, group_id)

    except Exception as e:
        print "error reading form data"
        print e
        return JsonWrapper.get_json(True, "error reading form data")

    return result


# get all groups for user 
@app.route("/group", methods=["GET"])
@login_required
def get_user_groups():

    group_id = None
    groups = None
    result = None

    try:
        user_id = current_user.get_id()

        groupDAO = GroupDAO()
        groups = groupDAO.get_all(user_id)
        groups = groups or []

        result = JsonWrapper.get_json(False, groups)

    except Exception as e:
        print "routes - get all groups"
        print e


    return result


# get a group
@app.route("/group/<group_id>", methods=["GET"])
@login_required
def get_group(group_id):

    groupDAO = GroupDAO()
    group = None
    result = None

    try:
        if group_id:
            group = groupDAO.get(group_id)

            if group:
                result = JsonWrapper.get_json(False, group)
            else:
                result = JsonWrapper.get_json(True, "No such group found")

        else:
            result = JsonWrapper.get_json(True, "Please supply the group id")

    except Exception as e:
        print " routes - get group by id"
        print e

    return result



# delete a group
@app.route("/group/<group_id>", methods=["DELETE"])
@login_required
def delete_group(group_id):

    groupDAO = GroupDAO()
    result = None

    try:
        if group_id:
            is_success = groupDAO.delete(group_id)

            if is_success:
                result = JsonWrapper.get_json(False)
            else:
                result = JsonWrapper.get_json(True, "Error deleting group")

        else:
            result = JsonWrapper.get_json(True, "Please supply the group id")

    except Exception as e:
        print "routes - delete group by id"
        print e

    return result


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
        post.tags = []

        if tags:
            tags = tags.split(",")
            # convert tags to list
            for word in tags:
                stripped = word.strip()

                if len(stripped) > 0:
                    post.tags.append(stripped)

        post.added_by = user_id
        post.date = datetime.utcnow()

        post_mapper = PostDAO()
        is_success = post_mapper.create(post)

        if is_success:
            result = JsonWrapper.get_json(False, is_success)
        else:
            result = JsonWrapper.get_json(True, "Error creating post")

    except Exception as e:

       print "error while creating post"
       print e

    return result


@app.route("/post/<post_id>", methods=["GET"])
@login_required
def get_post(post_id):

    post = None 
    user_id = current_user.get_id()
    result = None

    if post_id:

        try:

            post_mapper = PostDAO()
            post = post_mapper.get(post_id)

            result = JsonWrapper.get_json(False, post)

        except Exception as e:

            print "Error getting specific post"
            print e

    else:

        result = JsonWrapper.get_json(True, "Please supply post_id")

    return result


