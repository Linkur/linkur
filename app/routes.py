
from flask import request, make_response, send_file, session

from app import app
from DAO.userDAO import UserDAO
from DAO.groupDAO import GroupDAO
from DAO.postDAO import PostDAO
from model.user import User
from model.group import Group
from model.post import Post

# display index.html
@app.route("/")
def index():
    return send_file("static/index.html")


# login the user
@app.route("/login", methods=["POST"])
def login():

    # check if user is already logged in
    if "user" in session:
        return "User already logged in"

    # initialize variables
    email = None
    password = None
    userDAO = UserDAO(app.secret_key)

    try:
        # read form data
        email = request.form["email"]
        password = request.form["password"]
   
    except Exception as e:

        print "Error while reading form data"
        print e

        return "form data error"

    if email and password:
        if len(email.strip()) == 0:
            # email is blank
            return "Enter EMail"

        # validate if the email & password
        user = userDAO.validate(email, password)

        if user == None:
            # user not found
            return "User not found"

        else:
            # user found, create a session
            session["user"] = email
            return "log in success"

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
