
import psycopg2

from app.model.group import Group
from util import Util
import conf

class GroupDAO:

    def __init__(self):

        # get db connection instance
        self.db = psycopg2.connect(database=conf.PG_DB, host=conf.PG_HOST, user=conf.PG_USER, password=conf.PG_PASSWORD, port=conf.PG_PORT)


    # method to create a new group
    def add(self, group_name, user_id):

        result = None
        cur = self.db.cursor()

        # generate uuid for group
        group_id = Util.generate_uuid(group_name)
        if group_id == None:
            return None

        try:

            cur.execute("INSERT INTO public.groups (id, title) VALUES (%s,%s)",
                    (
                        group_id,
                        group_name
                    ))

            if cur.rowcount == 1:
                # get the last insert id
                # insert user and group combo tp user group table
                #SELECT * from public.groups ORDER BY id DESC LIMIT 1
                self.db.commit()
                cur.execute("SELECT id FROM public.groups ORDER BY id \
                                DESC LIMIT 1")
                row = cur.fetchone()
                result = row[0]

        except Exception as e:

            print "An error occured while creating group"
            print e

            # rollback DB
            self.db.rollback()
            return None

        finally:
        
            cur.close()
            return result


    def associate_user(self, user_id, group_id):
        
        result = None
        cur = self.db.cursor()

        try:

            cur.execute("INSERT INTO public.user_groups (user_id, group_id) \
                            VALUES (%s,%s)", ( user_id, group_id))

            if cur.rowcount == 1:

                result = True

        except Exception as e:

            print "error creating user group association"
            print e

            self.db.rollback()
            result = None

        finally:
            
            self.db.commit()
            cur.close()

            return result


    # method to delete a user-group association
    def remove_user_association(self, user_id, group_id):

        cur = self.db.cursor()

        try:

            cur.execute("DELETE FROM public.user_groups WHERE user_id = %s \
                            AND group_id = %s", (user_id, group_id))

        except Exception as e:

            print "An error occurred while deleting group"
            print e

            self.db.rollback()
            return False

        self.db.commit()
        cur.close()
        return True


    # method to delete a group
    def delete(self, group_id):

        result = None
        cur = self.db.cursor()

        try:

            cur.execute("DELETE FROM public.groups WHERE id = %s", (group_id))

            if cur.rowcount == 1:
                result = True

        except Exception as e:

            print "An error occurred while deleting group"
            print e

            self.db.rollback()
            result = None

        self.db.commit()
        cur.close()
        return result

