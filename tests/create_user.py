
# file to add tests for userDAO.py
import uuid
import psycopg2.extras

import sys
sys.path.append("../")
from app.DAO.userDAO import UserDAO
from app.model.user import User


def test_nose():
    assert True, "Nose success"

# test to create a user
def test_user_create():

    user = User("tester@test.com", "test123", "tester")

    user_mapper = UserDAO("LOL")
    assert user_mapper.add(user)

test_user_create()

