
from flask import request, make_response, send_file, session

from app import app
from DAO.userDAO import UserDAO
from DAO.groupDAO import GroupDAO
from DAO.postDAO import PostDAO
from model.user import User
from model.group import Group
from model.post import Post

@app.route("/")
def index():
    return send_file("static/index.html")


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

