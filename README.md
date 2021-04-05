# Serverless WebSockets in AWS

## Install serverless CLI

https://www.serverless.com/framework/docs/getting-started/

## Setup AWS Credentials

http://slss.io/aws-creds-setup

## Setup virtual environment with Python 3.6

https://docs.python.org/3.6/library/venv.html

## Install pip requirements 

`pip install -r requirements.txt`

## Install node modules

`npm install`

## Setup environment variables 
```
AWS_ACCESS_KEY_ID='<AWS_ACCESS_KEY>'
AWS_SECRET_ACCESS_KEY='<AWS_SECRET_ACCESS_KEY>'
AWS_DEFAULT_REGION='<AWS_REGION>' 

AWS_COGNITO_USER_POOL='<AWS_COGNITO_USER_POOL_ID>'
AWS_COGNITO_CLIENT_ID='<AWS_COGNITO_CLIENT_ID>'
AWS_COGNITO_REGION='<AWS_REGION>'
WSS_ENDPOINT='https://<API_GATEWAY_WEBSOCKET_ID>.execute-api.<AWS_REGION>.amazonaws.com/development'

```

## Deploy
`serverless deploy`

## Resources 

### Serverless Framework Documentation
https://www.serverless.com/framework/docs/

### Amazon API Gateway

#### Working with WebSocket APIs
https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api.html

### API Gateway quotas for configuring and running a WebSocket API
https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html#apigateway-execution-service-websocket-limits-table

### Amazon DynamoDB
https://aws.amazon.com/dynamodb/

### Amazon Cognito
https://aws.amazon.com/cognito/


## Author
### Asen Bozhilov
- https://github.com/abozhilov
- https://www.linkedin.com/in/asen-bozhilov-64643527/