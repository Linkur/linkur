
import psycopg2
import psycopg2.extras
import uuid
import conf
import hashlib
import random
import string

from app.model.user import User
from util import Util

class UserDAO:

    def __init__(self, secret_key):

        # Connect to db
        self.db = psycopg2.connect(
                                    database=conf.PG_DB, 
                                    host=conf.PG_HOST, 
                                    port=conf.PG_PORT, 
                                    user=conf.PG_USER, 
                                    password=conf.PG_PASSWORD
                                  )

        # store the scret key in the instance
        self.secret_key = secret_key
        # convert unicode to ascii string
        self.secret_key = self.secret_key.encode('base-64')
        self.util = Util()


    # util method to encrypt password
    def make_password_hash(self, password):
        
        salted_password = password+self.secret_key
        return hashlib.sha1(salted_password).hexdigest()


    # Add new user to DB
    def add(self, user):
        
        # encrypt the user password
        password_hash = self.make_pw_hash(user.password)
        user_id = Util.generate_uuid(user.email)

        try:
            cur = self.db.cursor()
            cur.execute("INSERT INTO public.users (id, email, name, password) \
                                VALUES (%s,%s,%s,%s)", 
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
        
        cur = None
        # get the user object for the email
        user = self.get(email)

        if user == None:
            print "User not found"
            return False 

        # check if the old passwords match
        if self.make_password_hash(password) == user.password:
            
            try:
                # create hash for new password
                new_password = self.make_password_hash(new_password)

                cur = self.db.cursor()
                cur.execute("UPDATE public.users SET password = %s \
                              WHERE ID = %s", 
                                  (
                                    new_password, 
                                    user.id
                                  )
                            )

                if cur.rowcount == 1:
                    self.db.commit()
                    return True
                else:
                    self.db.commit()
                    return False 

            except Exception as e:

                print "An error occured while updating password"
                print e

                self.db.rollback()
                return None

        else:

            print "Password does not match"
            return False


    def change_name(self, name, user_id):

        try:
            cur = self.db.cursor()
            cur.execute("UPDATE public.users SET NAME = '%s' \
                          WHERE ID = '%s'",
                                          (
                                              name,
                                              user_id
                                          )
                        )

        except Exception as e:

            print "Error changing user name"
            print e
            
            self.db.rollback()
            return False

        self.db.commit()
        return True


    # method to get the user object from db for a given email
    def get(self, email):
        
        user = User()
        try:
            cur = self.db.cursor()

            cur.execute("SELECT * FROM public.users \
                          WHERE email = %s", (email,))

            row = cur.fetchone()
            # build the user object
            # get the user id & convert it to python UUID type
            user.id = uuid.UUID(row[0])
            user.name = row[1]
            user.email = row[2]
            user.password = row[3]

        except Exception as e:

            print "An error occurred while reading user id"
            print e
            
            return None

        # return user object
        return user
        

    # method to validate if the email and password
    def validate(self, email, password):
        
        user = self.get(email)
        
        # check the hash of user input with the password from db
        hashed_pwd = self.make_password_hash(password)
        if hashed_pwd == user.password:
            return user

        else:
            return None

