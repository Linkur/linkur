
import psycopg2

class PostDAO:

    def __init__(self):
        
        # get the DB connection
        # ToDo add config file to read the connect details
        self.db = psycopg2.connect('user=linkur password=ayegivak dbname=linkur host=localhost port=5432')

    def get_all_posts_for_user(self, user_id):

        try:
            # Get the db cursor & execute the Select query
            cur = self.db.cursor();

            cur.execute("SELECT * FROM linkur where user_id = %s", (user_id, ))


     
