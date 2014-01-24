
import psycopg2.extras
import uuid
import datetime

class Util:

    @staticmethod 
    def generate_uuid(data):
        uuuid = None
        if data == None:
            print "data is none for uuid generation"
            return None
        
        try:

            data = data+str(datetime.datetime.now())
            #convert to ascii format string
            data = data.encode("base-64")

            # generate uuid based on DNS & sha1
            uid = uuid.uuid5(uuid.NAMESPACE_DNS, data)

            print uid
            # adapt py uuid to postgres uuid type
            uuuid = psycopg2.extras.UUID_adapter(uid)

        except Exception as e:
            
            print "error generating uuid"
            print e
            return None
        
        return uuuid



    def adapt_uuid(self, str_uuid):

        uid = uuid.UUID(str_uuid)
        uid = psycopg2.extras.UUID_adapter(uid);

        return uid
