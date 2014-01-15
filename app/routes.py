
from flask import request, make_response, send_file

from app import app
from model import user, post, group
from DAO import userDAO, groupDAO, postDAO


print "all imports fine"

@app.route("/")
def index():
    return send_file("static/index.html")

