
from flask import Flask
import conf

# create flask app
app = Flask(__name__)
app.secret_key = conf.SECRET_KEY

from app import routes

