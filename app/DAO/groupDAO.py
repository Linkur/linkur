
import psycopg2

from app.model.group import Group
from util import Util
import conf

class GroupDAO:

    def __init__(self):

        # get db connection instance
        self.db = psycopg2.connect(database=conf.PG_DB, host=conf.PG_HOST, user=conf.PG_USER, password=conf.PG_PASSWORD, port=conf.PG_PORT)
        # get a util instance
        self.util = Util()


    # method to create a new group
    def add_group(self, group):

        # generate uuid for group
        group_id = self.util.generate_uuid(group.title)

        try:

            # get db cursor
            cur = self.db.cursor()
            cur.execute("INSERT INTO public.groups (id, title) VALUES (%s,%s)",
                    (
                        group_id,
                        group.title
                    ))

        except Exception as e:

            print "An error occured while creating group"
            print e

            # rollback DB
            self.db.rollback()
            return False

        # successful insert -> commit changes
        self.db.commit()
        return True


    # method to change group name
    def change_group_name(self, group):

        try:
        
            # get db cursor
            cur = self.db.cursor()
            cur.execute("UPDATE public.groups SET TITLE = %s WHERE id=%s", (group.name, group.id))

        except Exception as e:

            print "An error occurred while updating group name"
            print e

            self.db.rollback()
            return False

        # successful update -> commit changes
        self.db.commit()
        return True


    # method to delete a group
    def delete_group(self, group_id):

        try:

            cur = self.db.cursor()
            cur.execute("DELETE FROM public.groups WHERE id = %s", (group_id))

        except Exception as e:

            print "An error occurred while deleting group"
            print e

            self.db.rollback()
            return False

        self.db.commit()
        return True

