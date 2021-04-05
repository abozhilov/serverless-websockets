import argparse
import os

import boto3


def authenticate_and_get_token(username, password):
    client = boto3.client('cognito-idp')

    resp = client.admin_initiate_auth(
        UserPoolId=os.getenv('AWS_COGNITO_USER_POOL'),
        ClientId=os.getenv('AWS_COGNITO_CLIENT_ID'),
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )

    print("Log in success")
    print("Id token:", resp['AuthenticationResult']['IdToken'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--user', help='Cognito username', required=True)
    parser.add_argument('--password', help='Cognito password', required=True)

    args = parser.parse_args()

    authenticate_and_get_token(args.user, args.password)