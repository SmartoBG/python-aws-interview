import os
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddbclient = boto3.client('dynamodb', endpoint_url='http://dynamodb:8000/')
 

def lambda_handler(event, context):
    try:
        response = ddbclient.batch_write_item(
        RequestItems={
            os.environ['DDBTableName']: [
                {
                    'PutRequest': {
                        'Item': {
                            'make': {'S': 'Nissan'},
                            'model': {'S': 'Micra'},
                            'year': {'N': '2004'},
                            'chassis_no': {'S': '12345A'},
                            'id': {'N': '1'},
                            'last_updated': {'S': '2017-02-01 00:00:00'},
                            'price': {'N': '500.0'}
                        }
                    }
                }
            ]}
        )

        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps({
                'message': 'Filled DynamoDB',
            }),
        }

    except ddbclient.exceptions.ResourceNotFoundException as e:
        logging.error('Cannot do operations on a non-existent table')
        raise e
    except ClientError as e:
        logging.error('Unexpected error')
        raise e

