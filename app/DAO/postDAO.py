
import conf
import psycopg2
import hashlib
import random
import string

from model.user import User


class PostDAO:

    def __init__(self):

        # Connect to db
        self.db = psycopg2.connect(database=conf.PG_DB, host=conf.PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)

    def get_all_posts_for_user(self, user_id):

        try:
            # Get the db cursor & execute the Select query
            cur = self.db.cursor();

            cur.execute("SELECT * FROM linkur where user_id = %s", (user_id, ))

        except Exception as e:

            print "Error occured reading posts"
            print e

            return False

        return True

