import json


def lambda_handler(event, context):
    ret = {"state": {}, "schema": {}, "insert": {}, "hasMore": False}

    return json.dumps(ret)
