import json

class JsonWrapper:

    @staticmethod
    def get_json(error, result=None):
        # convert dictionary to JSON format
        response = {}
        response['error'] = error

        if result and type(result.__str__()) == dict:
            response['data'] = result.__str__()

        elif result and type(result) == list:

            items = []

            for item in result:
                items.append(item.__str__())

            response['data'] = items

        
        if not error and result == None:
            response['data'] = "OK"

        return json.dumps(response)

