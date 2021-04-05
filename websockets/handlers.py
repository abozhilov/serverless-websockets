import logging

from websockets import utils

logger = logging.getLogger('websockets.api')
logger.setLevel(logging.DEBUG)


def handle_connect(event, context):
    """
    Handle new WebSocket connection.
    Add email and connection_id in connections pool
    """
    request_context = event['requestContext']
    username = request_context['authorizer']['principalId']
    connection_id = request_context['connectionId']

    logger.info(f'Adding connection: {connection_id} for username: {username}')

    utils.add_connection(connection_id, username)

    return utils.response('Connect')


def handle_disconnect(event, context):
    """
    Handle WebSocket disconnect.
    Cleanup username and connection_id from the connections pool.
    """
    request_context = event['requestContext']
    connection_id = request_context['connectionId']

    logger.info(f'Removing connection: {connection_id}')

    utils.remove_connection(connection_id)

    return utils.response('Disconnect')


def handle_message(event, context):
    """
    Handle new message via WebSocket connection.
    """
    request_context = event['requestContext']
    username = request_context['authorizer']['principalId']
    connection_id = request_context['connectionId']

    if request_context['eventType'] == 'MESSAGE':
        connections = utils.get_all_connections()

        logger.info(f'Broadcasting user message from username {username}')

        for x in connections:
            if x['connection_id'] != connection_id:
                utils.send_message(x['connection_id'], username, event['body'])

    return utils.response('Message')


