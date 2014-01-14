
import psycopg2

from model.group import Group
from util import Util
import conf

# data mapper class for user_group_subscription table
class UserPostDAO:

    def __init__(self):

        self.db = psycopg2.connect(dbname=conf.PG_DB, host=conf.PG_HOST, user=conf.PG_USER, password=conf.PG_PASSWORD, port=conf.PG_PORT)
        self.util = Util()


# method to add a record in user_subscription table
    def add_user_post(self, user_id, post_id):

        try:

            # get db cursor
            cur = self.db.cursor()
            cur.execute("INSERT INTO user_reading_list VALUES (%s,%s)",
                    (
                        user_id,
                        post_id
                        ))

        except Exception as e:

            print "An error occurred while inserting into user_reading_list"
            print e
            
            # rollback db
            self.db.rollback()
            return False

        # commit db changes
        self.db.commit()
        return True


# method to delete a record in user_subscription table
    def delete_user_post(self, user_id, post_id):

        try:
            
            # get db cursor
            cur = self.db.cursor()
            cur.execute("DELETE FROM public.user_reading_list VALUES (%s,%s)",
                    (
                        user_id,
                        post_id
                        ))

            except Exception as e:

                print "An error occurred while deleting entry form user_reading_list"
                print e

                # rollback db
                self.db.rollback()
                return False

            # commit db changes
            self.db.commit()
            return True

