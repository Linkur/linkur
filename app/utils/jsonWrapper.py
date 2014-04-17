import json

class JsonWrapper:

    @staticmethod
    def get_json(error, result=None):
        # convert dictionary to JSON format
        response = {}
        response['error'] = error

        if result and type(result.serialize()) == dict:
            response['data'] = result.serialize()

        elif result and type(result) == list:

            items = []

            for item in result:
                items.append(item.serialize())

            response['data'] = items

        
        if not error and result == None:
            response['data'] = "OK"

        return json.dumps(response)

