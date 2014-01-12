
# file to add tests for userDAO.py
from app.DAO.userDAO import UserDAO
from app.model.user import User
import conf

# test to create a user
def user_create():

    user = User()
    user['name'] = "dev"
    user['password'] = "dev123"
    user["email"] = "dev@dev.com"

    user_mapper = UserDAO()
    user_mapper.add_user()

user_create()
