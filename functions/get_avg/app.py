import os
import simplejson as json # type: ignore
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.types import NULL, TypeDeserializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ddbclient = boto3.client('dynamodb', endpoint_url='http://dynamodb:8000/')
TABLENAME = os.environ['DDBTableName']

def lambda_handler(event, context):
    
    try:
        response = ddbclient.scan(
            TableName=TABLENAME,
            Select='SPECIFIC_ATTRIBUTES',
            ProjectionExpression='price',
        )
        
        #logging.info(response)
        items = response['Items']
        if len(items) > 0:
            lst = [TypeDeserializer().deserialize(x['price']) for x in items if x]  # type: ignore 
            avg = sum(lst)/len(lst)
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'headers': { 
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'
                },
                'body': json.dumps(avg)
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