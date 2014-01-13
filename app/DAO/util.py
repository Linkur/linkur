
import psycopg2.extras
import uuid
import datetime

class Util:

    
    def generate_uuid(self, data):
        uuuid = None
        
        try:

            # generate uuid based on DNS & sha1
            uid = uuid.uuid5(uuid.NAMESPACE_DNS, data+str(datetime.datetime.now))

            # adapt py uuid to postgres uuid type
            uuuid = psycopg2.extras.UUID_adapter(uid)

        except Exception as e:
            
            print "error generating uuid"
            return None
        
        return uuuid



    def adapt_uuid(self, str_uuid):

        uid = uuid.UUID(str_uuid)
        uid = psycopg2.extras.UUID_adapter(uid);

        return uid
