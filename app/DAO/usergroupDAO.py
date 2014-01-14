
import psycopg2

from model.group import Group
from util import Util
import conf

# data mapper class for user_group_subscription table
class UserGroupDAO:

    def __init__(self):

        self.db = psycopg2.connect(dbname=conf.PG_DB, host=conf.PG_HOST, user=conf.PG_USER, password=conf.PG_PASSWORD, port=conf.PG_PORT)
        self.util = Util()


    def add_user_group(self, user_id, group_id):

        try:

            cur = self.db.cursor()
            cur.execute("INSERT INTO public.user_group_subscription (USER_ID, GROUP_ID) VALUES (%s,%s)",
                    (
                        user_id,
                        group_id
                    ))

        except Exception as e:

            print "An error occurred adding user group subscription"
            print e

            # rollback db
            self.db.rollback()
            return False

        self.db.commit()
        return True


    # remove group from user
    def remove_user_group(self, user_id, group_id):

        try:

            # get db cursor
            cur = self.db.cursor()
            cur.execute("DELETE FROM public.user_group_subscription WHERE USER_ID = %s AND GROUP_ID = %s", 
                    (
                        user_id,
                        group_id
                    ))
            
        except Exception as e:

            print "An occured while remove group for user"
            print e

            # rollback db
            self.db.rollback()
            return False

        # commit db changes
        self.db.commit()
        return True

