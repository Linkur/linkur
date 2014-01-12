
import psycopg2
import conf
import hashlib
import random
import string

from model.user import User
from util import Util

class UserDAO:

    def __init__(self):

        # Connect to db
        self.db = psycopg2.connect(database=conf.PG_DB, host=conf.PG_HOST, port=conf.PG_PORT, user=conf.PG_USER, password=conf.PG_PASSWORD)


    # util method to create a random salt
    def make_salt(self):

        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        
        return salt


    # util method to encrypt password
    def make_pw_hash(self, pw, salt=None):

        if salt == None:
            salt = self.make_salt()
        return hashlib.sha1(pw + salt).hexdigest()+","+salt


    # Add new user to DB
    def add_user(self, user):
        
        # encrypt the user password
        password_hash = self.make_pw_hash(user.password)

        util = Util()
        user_id = util.make_uuid(user.email)

        try:
            cur = self.db.cursor()
            cur.execute("INSERT INTO public.users (id, email, name, password) VALUES (%s,%s,%s,%s)", 
                (
                    user_id,
                    user.email,
                    user.name,
                    password_hash 
                    )
                )

        except Exception as e:

            print "Error creating user"
            print e
            
            # An error occurred, rollback db
            self.db.rollback()
            return False
        
        self.db.commit()
        return True
   
   
    # method to change the user password
    def change_password(self, user_id, password, new_password):
        
        # encrypt the new password
        new_password_hash = self.make_pwd_hash(new_password)

        try:
            cur = self.cursor()
            cur.execute("UPDATE public.users SET PASSWORD = '%s' WHERE ID = '%s'",
                    (
                        new_password,
                        user('id')
                    ))

        except Exception as e:

            print "Error ocurred updating user password"
            print e

            # An error occurred, rollback db
            db.rollback()
            return False

        db.commit()
        return True

