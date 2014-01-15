
from flask import Flask

# create flask app
app = Flask(__name__)


from app import routes
