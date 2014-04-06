
import psycopg2
import psycopg2.extras
import conf
import uuid
import hashlib
from os import urandom
import string

from flask_login import UserMixin

from app.model.user import User

class UserDAO:

    def __init__(self):

        # Connect to db
        self.db = psycopg2.connect(
                                    database=conf.PG_DB, 
                                    host=conf.PG_HOST, 
                                    port=conf.PG_PORT, 
                                    user=conf.PG_USER, 
                                    password=conf.PG_PASSWORD
                                  )


    # util method to encrypt password
    def make_password_hash(self, password, salt=None):
        
        if salt == None:
            salt = urandom(24)
            salt = salt.encode('base-64')

        salted_password = salt+password

        hashed_password = hashlib.sha256(salted_password).hexdigest()+','+salt
        return hashed_password


    # Add new user to DB
    def add(self, user):
        
        result = None
        cur = self.db.cursor()
        # encrypt the user password
        password_hash = self.make_password_hash(user.password)
        print "pass len ",len(password_hash)
        try:
            cur.execute("INSERT INTO public.users ( email, name, password) \
                                VALUES (%s,%s,%s) RETURNING id",
                                                    (
                                                        user.email,
                                                        user.name,
                                                        password_hash 
                                                    ))

            if cur.rowcount == 1:
                row = cur.fetchone()
                self.db.commit()
                result = row[0]

        except Exception as e:

            print "Error creating user"
            print e
            
            # An error occurred, rollback db
            self.db.rollback()
       
        finally:
            
            cur.close()
            return result
   
   
    # method to change the user password
    def change_password(self, email, password, new_password):
        
        result = None
        cur = None
        # get the user object for the email
        user = self.get_by_email(email)

        if user == None:
            print "User not found"
            return result

        salt = user.password.split(',')[1]
        # check if the old passwords match
        if self.make_password_hash(password, salt) == user.password:
            
            try:
                # create hash for new password
                new_password = self.make_password_hash(new_password)

                cur = self.db.cursor()
                cur.execute("UPDATE public.users SET password = %s \
                              WHERE ID = %s RETURNING id", 
                                  (
                                    new_password, 
                                    user.id
                                  )
                            )

                if cur.rowcount == 1:
                    row = cur.fetchone()
                    self.db.commit()
                    result = row[0]

            except Exception as e:

                print "An error occured while updating password"
                print e

                self.db.rollback()
                result = True

            finally:

                cur.close()
                return result

        else:

            print "Password does not match"
            return result


    # method to get the user object from db for a given email
    def get_by_email(self, email):
        
        
        cur = self.db.cursor()
        user = None

        psycopg2.extras.register_uuid()
        try:

            cur.execute("SELECT * FROM public.users \
                          WHERE email = %s", (email,))

            if cur.rowcount > 0:
                row = cur.fetchone()
                # build the user object
                # get the user id & convert it to python UUID type

                user = User()
                user.id = row[0]
                user.name = row[1]
                user.email = row[2]
                user.password = row[3]

        except Exception as e:

            print "An error occurred while reading user id"
            print e
            user = None
        
        finally:
            # return user object
            return user
        

    # method to get the user object from db for a given id
    def get(self, id):
        
        
        cur = self.db.cursor()
        user = None

        psycopg2.extras.register_uuid()
        try:

            cur.execute("SELECT * FROM public.users \
                          WHERE id = %s", (id,))

            row = cur.fetchone()
            # build the user object
            # get the user id & convert it to python UUID type

            user = User()
            user.id = row[0]
            user.name = row[1]
            user.email = row[2]
            user.password = row[3]

        except Exception as e:

            print "An error occurred while reading user id"
            print e
            
            return None
        
        finally:
            # return user object
            return user


    # method to validate if the email and password
    def validate(self, email, password):
        
        user = self.get_by_email(email)
        #User in DB
        if user:
            # check the hash of user input with the password from db
        # check the hash of user input with the password from db
            salt = user.password.split(',')[1]
            hashed_pwd = self.make_password_hash(password,salt)
            if hashed_pwd == user.password:
                return user

            #password does not match
            else:
                return None

        #User not in DB
        else:
            return None

    
    def delete(self, user_id):

        result = None
        cur = None
        psycopg2.extras.register_uuid()

        try:

            cur = self.db.cursor()
            print "deleting ", user_id
            cur.execute("DELETE FROM public.users WHERE id = %s", (user_id,))

            if cur.rowcount == 1:
                self.db.commit()
                result = True

        except Exception as e:

            print "Error deleting user"
            print e

            self.db.rollback()

        finally:

            cur.close()
            return result
    

    def __del__(self):

        self.db.close()

