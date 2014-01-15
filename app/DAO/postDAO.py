
import conf
import psycopg2
import hashlib
import random
import string

from app.model.user import User


class PostDAO:

    def __init__(self):

        # Connect to db
        self.db = psycopg2.connect(database=conf.PG_DB, host=conf.PG_HOST, port=conf.PG_PORT, user=conf.PG_USER, password=conf.PG_PASSWORD)

    def get_posts_for_group(self, user_id, group_id):

        try:
            # Get the db cursor & execute the Select query
            cur = self.db.cursor();

            cur.execute("SELECT * FROM linkur where user_id = %s", (user_id, ))

        except Exception as e:

            print "Error occured reading posts"
            print e

            return False

        return True

    def create_post(self, post):

        try:

            cur = self.db.cursor()
            cur.execute("INSERT INTO public.posts (ID, TITLE, LINK, GROUP_ID, TAGS, ADDED_BY, DATE) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            (
                                post.id,
                                post.title,
                                post.link,
                                post.group,
                                post.tags,
                                post.added_by,
                                post.date
                            ))

        except Exception as e:

            print "An error occured while inserting post"
            print e

            self.db.rollback()
            return False

        self.db.commit()
        return True

