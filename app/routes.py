
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

    email = None
    password = None
    userDAO = UserDAO(app.secret_key)

    try:
        email = request.form["email"]
        password = request.form["password"]
   
    except Exception as e:

        print "Error while reading form data"
        print e

        return "form data error"

    if email and password:
        print email, password
        if len(email.strip()) == 0:
            return "Enter EMail"

        user = userDAO.validate(email, password)
        print user.password
        if user == None:
            return "User not found"

        else:
            session["user"] = email
            return "log in success"

    else:

        return "email / password error"

