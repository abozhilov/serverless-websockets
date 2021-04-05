import json

from websockets import utils


def push_message(event, context):
    """
    Broadcast a message to all connections via websockets
    """
    body = event.get('body', None)

    if body is None:
        return utils.response('Missing message', utils.STATUS_BAD_REQUEST)

    message = json.loads(body)
    connections = utils.get_all_connections()

    for x in connections:
        utils.send_system_message(x['connection_id'], message)

    return utils.response('OK')