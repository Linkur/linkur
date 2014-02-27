
import psycopg2

from app.model.group import Group
import conf

class GroupDAO:

    def __init__(self):

        # get db connection instance
        self.db = psycopg2.connect(database=conf.PG_DB, host=conf.PG_HOST, user=conf.PG_USER, password=conf.PG_PASSWORD, port=conf.PG_PORT)


    # method to create a new group
    def create(self, group_name):

        result = None
        cur = self.db.cursor()
        psycopg2.extras.register_uuid()

        try:

            cur.execute("INSERT INTO public.groups (title) VALUES (%s) \
                    RETURNING id", ( group_name,))

            if cur.rowcount == 1:
                # get the last insert id
                # insert user and group combo to user group table
                row = cur.fetchone()
                result = row[0]

        except Exception as e:

            print "An error occured while creating group"
            print e

            # rollback DB
            self.db.rollback()
            return None

        finally:
        
            self.db.commit()
            cur.close()
            return result


    def associate_user(self, user_id, group_id):
        
        result = None
        cur = self.db.cursor()
        psycopg2.extras.register_uuid()

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


    def add(self, group_name, user_id):
       
        result = None
        # Create a group with the given name
        group_id = self.create(group_name)
        
        # on successful group creation, create user - group association
        if group_id != None:
            result = self.associate_user(user_id, group_id)

            # on successful association, return group id
            if result != None:
                result = group_id

            # on error creating association, delete created group
            else:
                print "Error creating association, deleting the created group"
                self.delete(group_id)

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

            cur.execute("DELETE FROM public.groups WHERE id = %s", (group_id,))

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

