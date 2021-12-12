import os
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ddbclient = boto3.client('dynamodb', endpoint_url='http://dynamodb:8000/')

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']
    last_updated = event['queryStringParameters']['last_updated']

    try:
        response = ddbclient.get_item(
            TableName=os.environ['DDBTableName'],
            Key={
                'id':{'N': id},
                'last_updated':{'S': last_updated}
            },
            AttributesToGet=[
                'year', 'price', 'model', 'make'
            ],
        )
        
        logging.info(response)

        if response:
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'headers': { 
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'
                },
                'body': json.dumps({
                    'message': response,
                }),
            }
        else:
            return {
                'statusCode': '404',
                'headers': { 
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'
                },
                'body': json.dumps({
                    'message': 'Item not found',
                }),
            }
    except ddbclient.exceptions.ResourceNotFoundException as e:
        logging.error('Cannot do operations on a non-existent table')
        raise e
    except ClientError as e:
        logging.error('Unexpected error')
        raise e