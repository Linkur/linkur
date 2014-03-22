
# file to add tests for userDAO.py
import uuid
import psycopg2.extras

import sys
sys.path.append("../")
from app.DAO.userDAO import UserDAO
from app.model.user import User


def test_nose():
    assert True, "Nose success"

def test_delete_user():

    user_mapper = UserDAO("LOL")
    user = user_mapper.get_by_email("tester@test.com")
    assert user_mapper.delete(user.id)

