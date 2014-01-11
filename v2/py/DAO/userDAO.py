
import hashlib
import random
import string

from model.user import User


class UserDAO:

    def __init__(self):

        # Connect to db
        self.db = psycopg2.connect('dbname=linkur user=postgres password=postgres host=localhost port=5432')


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
        password_hash = self.make_pw_hash(user['password'])
        
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO public.users (id, email, name, password) VALUES (%s,%s,%s,%s)", 
                (
                    user['id'],
                    user['email'],
                    user['name'],
                    password_hash 
                    )
                )

        except Exceptions as e:

            print "Error creating user"
            print e
            
            # An error occurred, rollback db
            db.rollback()
            return False
        
        db.commit()
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
                    )

        except Exception as e:

            print "Error ocurred updating user password"
            print e

            # An error occurred, rollback db
            db.rollback()
            return False

        db.commit()
        return True

