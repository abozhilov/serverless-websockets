import logging

import jwt

from authentication import utils
from settings import settings


def cognito_auth(event, context):
    token = utils.get_auth_token(event)

    if token is None:
        return utils.generate_policy(None, False, event['methodArn'])

    try:
        claims = utils.get_claims(
            settings.AWS_COGNITO_REGION,
            settings.AWS_COGNITO_USER_POOL,
            token,
            settings.AWS_COGNITO_CLIENT_ID
        )

        return utils.generate_policy(claims['email'], True, event['methodArn'])

    except jwt.exceptions.InvalidTokenError as e:
        logging.error(f'InvalidTokenError: {e}')
        return utils.generate_policy(None, False, event['methodArn'])

    except Exception as e:
        logging.error(f'Other error: {e}')
        return utils.generate_policy(None, False, event['methodArn'])