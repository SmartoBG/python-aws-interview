import os
import simplejson as json # type: ignore
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ddbclient = boto3.client('dynamodb', endpoint_url='http://dynamodb:8000/')
TABLENAME = os.environ['DDBTableName']

def lambda_handler(event, context):
    id = event['queryStringParameters'].get('id', "")

    try:
        response = ddbclient.query(
            TableName=TABLENAME,
            KeyConditionExpression='id = :id',
            ExpressionAttributeNames = {
                '#yr': 'year'
            },
            ExpressionAttributeValues={
                ":id": {'N': id}
            },
            ProjectionExpression='#yr, price, model, make, last_updated',
            Limit=1,
            ScanIndexForward=False
        )
        
        #logging.info(response)

        if len(response['Items']) > 0:
            diction_items = {x: TypeDeserializer().deserialize(y) for x, y in response['Items'][0].items()}   # type: ignore
            print(diction_items)
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'headers': { 
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'
                },
                'body': json.dumps(diction_items)
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