import json
import logging

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

from settings import settings


STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_NOT_FOUND = 404
STATUS_SERVER_ERROR = 500


logger = logging.getLogger('websockets.api')
logger.setLevel(logging.DEBUG)

dynamo_db = boto3.resource('dynamodb')
gateway_api = boto3.client('apigatewaymanagementapi', endpoint_url=settings.WSS_ENDPOINT)


def add_connection(connection_id, username):
    """Add new connection and user_id in the connections pool"""
    connections_pool = dynamo_db.Table('ConnectionsPool')

    connections_pool.put_item(
        Item={
            'connection_id': connection_id,
            'username': username
        }
    )


def remove_connection(connection_id):
    """Cleanup user_id and connection_id from the connections pool."""
    connections_pool = dynamo_db.Table('ConnectionsPool')

    try:
        connections_pool.delete_item(
            Key={
                'connection_id': connection_id
            }
        )
    except ClientError as e:
        logger.error(e)


def get_all_connections():
    """Returns all active websocket connections"""
    connections_pool = dynamo_db.Table('ConnectionsPool')
    response = connections_pool.scan(ProjectionExpression='connection_id')

    return response.get('Items', [])


def send_message(connection_id, username, message):
    """Send message from user to specific connection"""
    data = {
        'type': 'user-message',
        'author': username,
        'message': message
    }

    return gateway_api.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))


def send_system_message(connection_id, message):
    """Send system message to specific connection"""
    data = {
        'type': 'system-message',
        'message': message
    }

    return gateway_api.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))


def response(body, status=STATUS_OK):
    return {
        'statusCode': status,
        'body': body
    }