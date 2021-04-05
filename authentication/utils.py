import base64
import six
import struct
import os
import json
import jwt
import requests
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


EVENT_TYPE_TOKEN = 'TOKEN'
EVENT_TYPE_REQUEST = 'REQUEST'

ALLOW = 'Allow'
DENY = 'Deny'


def intarr2long(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)


def base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")

    # urlsafe_b64decode will happily convert b64encoded data
    _d = base64.urlsafe_b64decode(bytes(data) + b'==')
    return intarr2long(struct.unpack('%sB' % len(_d), _d))


def pool_url(aws_region, aws_user_pool):
    """ Create an Amazon cognito issuer URL from a region and pool id
    Args:
        aws_region (string): The region the pool was created in.
        aws_user_pool (string): The Amazon pool ID.
    Returns:
        string: a URL
    """
    return f"https://cognito-idp.{aws_region}.amazonaws.com/{aws_user_pool}"


def aws_key_dict(aws_region, aws_user_pool):
    """ Fetches the AWS JWT validation file (if necessary) and then converts
    this file into a keyed dictionary that can be used to validate a web-token
    we've been passed and calculates the pem formatted keys
    Args:
        aws_user_pool (string): the ID for the user pool
    Returns:
        dict: a dictonary of values
    """
    filename = os.path.abspath(
        os.path.join(
            os.path.dirname('/tmp/'), 'aws_{}.json'.format(aws_user_pool)
        )
    )

    if not os.path.isfile(filename):
        # If we can't find the file already, try to download it.
        aws_data = requests.get(
            pool_url(aws_region, aws_user_pool) + '/.well-known/jwks.json'
        )
        aws_jwt = json.loads(aws_data.text)
        with open(filename, 'w+') as json_data:
            json_data.write(aws_data.text)
            json_data.close()

    else:
        with open(filename) as json_data:
            aws_jwt = json.load(json_data)
            json_data.close()

    # We want a dictionary keyed by the kid, not a list.
    result = {}
    for item in aws_jwt['keys']:
        exponent = base64_to_long(item['e'])
        modulus = base64_to_long(item['n'])
        numbers = RSAPublicNumbers(exponent, modulus)
        public_key = numbers.public_key(backend=default_backend())
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        item['pem'] = pem
        result[item['kid']] = item

    return result


def get_claims(aws_region, aws_user_pool, token, audience=None):
    """ Given a token (and optionally an audience), validate and
    return the claims for the token
    """
    # header, _, _ = get_token_segments(token)
    header = jwt.get_unverified_header(token)
    kid = header['kid']

    verify_url = pool_url(aws_region, aws_user_pool)

    keys = aws_key_dict(aws_region, aws_user_pool)

    key = keys.get(kid)['pem']

    kwargs = {
        'issuer': verify_url,
        'algorithms': [jwt.get_unverified_header(token)['alg']]
    }
    if audience is not None:
        kwargs['audience'] = audience

    print('Shit')

    # TODO: Confirm the error states here
    claims = jwt.decode(
        token,
        key,
        **kwargs,
    )

    return claims


def generate_policy(principal_id, allow, method_arn):
    auth_response = {'principalId': principal_id}

    if method_arn:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': ALLOW if allow else DENY,
                    'Resource': method_arn
                }
            ]
        }

        auth_response['policyDocument'] = policy_document

    return auth_response


def get_auth_token(event):
    token = None
    event_type = event['type']

    if event_type == EVENT_TYPE_TOKEN:
        token = event.get('authorizationToken', None)
    elif event_type == EVENT_TYPE_REQUEST:
        token = event['headers'].get('Authorization', None)

    return token
