
from flask import request, make_response, send_file, session, jsonify
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
    json_response = JsonResponse()

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
            json_response.error = True
            json_response.data = "params error"

    except Exception as e:
        print "error while signing up user"
        print e
        
        # 500 internal server error
        raise ExceptionResponse()

    if result:
        json_response.error = False
        json_response.data = "Success!"
    else:
        json_response.error = True
        json_response = "Error signing up user"

    return jsonify(json_response.to_dict())

# login the user
@app.route("/login", methods=["POST"])
def login():

    result = None
    email = request.form["email"]
    password = request.form["password"]
    json_response = JsonResponse()

    if email and password:
        email = email.lower()
        user_mapper = UserDAO()
        user = user_mapper.validate(email, password)

        if user:
            #login user
            is_success = login_user(user)
            if is_success:
                json_response.error = False
                json_response.data = "User logged in"
            else:
                json_response.error = True
                json_response.data = "Check user/password"

        else:
            json_response.error = True
            json_response.data = "Check user/password"

    else:
        json_response.error = True
        json_response.data = "email/password not supplied"

    return jsonify(json_response.to_dict())


# logout user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"error" : False, "data" : "User logged out"})


# create a group
@app.route("/groups", methods=["POST"])
@login_required
def create_group():

    group_id = None
    result = None
    json_response = JsonResponse()

    try:
        user_id = current_user.get_id()
        group_name = request.form["group_name"]

        if(len(group_name.strip()) == 0):
            return "Group name is blank"

        groupDAO = GroupDAO()
        group_id = groupDAO.add(group_name, user_id)

        json_response.error = False
        json_response.data = str(group_id)

    except Exception as e:
        print "error reading form data"
        print e
        
        # 500 internal server error
        return ExceptionResponse()

    return make_response(jsonify(json_response.to_dict()), 201)


# get all groups for user 
@app.route("/groups", methods=["GET"])
@login_required
def get_user_groups():

    group_id = None
    groups = None
    result = None
    json_response = JsonResponse()

    try:
        user_id = current_user.get_id()

        groupDAO = GroupDAO()
        groups = groupDAO.get_all(user_id)
        groups = groups or []

        if groups:
            json_response.error = False
            json_response.data = groups

    except Exception as e:
        print "routes - get all groups"
        print e
        
        # 500 internal server error
        raise ExceptionResponse()

    return jsonify(json_response.to_dict())


# get a group
@app.route("/groups/<group_id>", methods=["GET"])
@login_required
def get_group(group_id):

    groupDAO = GroupDAO()
    group = None
    result = None
    json_response = JsonResponse()

    try:
        if group_id:
            group = groupDAO.get(group_id)

            if group:
                json_response.error = False
                json_response.data = group
            else:
                raise 404

        else:
            raise 400

    except Exception as e:
        print " routes - get group by id"
        print e
        
        # 500 internal server error
        raise ExceptionResponse()

    return make_response(jsonify(json_response.to_dict()))



# delete a group
@app.route("/groups/<group_id>", methods=["DELETE"])
@login_required
def delete_group(group_id):

    groupDAO = GroupDAO()
    result = None
    json_response = JsonResponse()

    try:
        if group_id:
            is_success = groupDAO.delete(group_id)

            if is_success:
                json_response.error = False
                json_response.data = "OK"
            else:
                raise ExpectionResponse("Error deleting group")
        else:
            raise 400

    except Exception as e:
        print "routes - delete group by id"
        print e
        
        # 500 internal server error
        raise ExpectionResponse("Error deleting group")

    return jsonify(json_response.to_dict())


# create a new post
@app.route("/posts", methods=["POST"])
@login_required
def create_post():

    post = Post()
    user_id = current_user.get_id()
    result = None
    json_response = JsonResponse()

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
            json_response.error = False
            json_response.data = str(is_success)
        else:
            raise ExceptionResponse("Error creating post")

    except Exception as e:

       print "error while creating post"
       print e
       
        # 500 internal server error
       raise ExceptionResponse("Error creating post")

    return make_response(jsonify(json_response.to_dict()), 201)


# get post by id
@app.route("/posts/<post_id>", methods=["GET"])
@login_required
def get_post(post_id):

    post = None 
    user_id = current_user.get_id()
    result = None
    json_response = JsonResponse()

    if post_id:

        try:

            post_mapper = PostDAO()
            post = post_mapper.get(post_id)
            json_response.error = False
            json_response.data = post

        except Exception as e:

            print "Error getting specific post"
            print e
        
            # 500 internal server error
            raise ExceptionResponse()

    else:
        raise 400

    return jsonify(json_response.to_dict())


# get all posts for a group
@app.route("/groups/<group_id>/posts", methods=["GET"])
@login_required
def get_posts_for_group(group_id):

    post = None 
    user_id = current_user.get_id()
    result = None
    json_response = JsonResponse()

    if group_id:

        try:

            post_mapper = PostDAO()
            posts = post_mapper.get_posts_for_group(user_id, group_id)
            json_response.error = False
            json_response.data = posts

        except Exception as e:

            print "Error getting group posts"
            print e
        
            # 500 internal server error
            raise ExceptionResponse()

    else:
        raise 400

    return jsonify(json_response.to_dict())


# edit a post
@app.route("/posts/<post_id>", methods=["PUT"])
@login_required
def edit_post(post_id):

    user_id = current_user.get_id()
    result = None
    json_response = JsonResponse()

    if post_id:

        try:

            post_mapper = PostDAO()
            post = Post()
            post.id = request.form["id"]
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

            result = post_mapper.update(post, user_id)
            
            if result:
                json_response.error = False
                json_response.data = result
            else:
                json_response.error = True
                json_response.data = "Could not update post"

        except Exception as e:
            print "Error occurred while updating post"
            print e
            raise ExceptionResponse()

    else:
        raise 400

    return jsonify(json_response.to_dict())



class ExceptionResponse(Exception):

    def __init__(self, message=None):

        Exception.__init__(self)
        self.message = message or "Internal Server Error"

    def __dict__(self):

        rv = {}
        rv['error'] = 500
        rv['message'] = self.message
        return rv

class JsonResponse():

    def __init__(self, error_state=False, payload=None):
        self.error = error_state
        self.data = (payload or {})

    def to_dict(self):
        rv = {}
        rv['error'] = self.error
        rv['data'] = self.data
        return rv

@app.errorhandler(ExceptionResponse)
def internal_error(error):
    return make_response(jsonify(error.__dict__()), 500)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error" : "Not Found"}), 404)

@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify({"error" : "Unauthorized"}), 401)

