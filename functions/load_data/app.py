import os
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddbclient = boto3.client("dynamodb", endpoint_url="http://dynamodb:8000/")
TABLENAME = os.environ["DDBTableName"]


def lambda_handler(event, context):
    try:
        response = ddbclient.batch_write_item(
            RequestItems={
                TABLENAME: [
                    {
                        "PutRequest": {
                            "Item": {
                                "make": {"S": "Nissan"},
                                "model": {"S": "Micra"},
                                "year": {"N": "2004"},
                                "chassis_no": {"S": "12345A"},
                                "id": {"N": "1"},
                                "last_updated": {"S": "2017-02-01 00:00:00"},
                                "price": {"N": "500.0"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "make": {"S": "Nissan"},
                                "model": {"S": "Micra"},
                                "year": {"N": "2004"},
                                "chassis_no": {"S": "12345A"},
                                "id": {"N": "1"},
                                "last_updated": {"S": "2017-03-01 00:00:00"},
                                "price": {"N": "400.0"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "make": {"S": "Ford"},
                                "model": {"S": "Fiesta"},
                                "year": {"N": "2002"},
                                "chassis_no": {"S": "12345B"},
                                "id": {"N": "2"},
                                "last_updated": {"S": "2017-03-01 00:00:00"},
                                "price": {"N": "300.0"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "make": {"S": "Audi"},
                                "model": {"S": "A3"},
                                "chassis_no": {"S": "12345C"},
                                "id": {"N": "3"},
                                "last_updated": {"S": "2017-04-01 00:00:00"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "make": {"S": "Nissan"},
                                "model": {"S": "Micra"},
                                "year": {"N": "2004"},
                                "chassis_no": {"S": "12345D"},
                                "id": {"N": "4"},
                                "last_updated": {"S": "2017-05-01 00:00:00"},
                                "price": {"N": "200.0"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "make": {"S": "Peugeot"},
                                "model": {"S": "308"},
                                "year": {"N": "1998"},
                                "chassis_no": {"S": "12345E"},
                                "id": {"N": "5"},
                                "last_updated": {"S": "2017-06-01 00:00:00"},
                                "price": {"N": "100.0"},
                            }
                        }
                    },
                ]
            }
        )

        return {
            "statusCode": response["ResponseMetadata"]["HTTPStatusCode"],
            "body": json.dumps(
                {
                    "message": "Filled DynamoDB",
                }
            ),
        }

    except ddbclient.exceptions.ResourceNotFoundException as e:
        logging.error("Cannot do operations on a non-existent table")
        raise e
    except ClientError as e:
        logging.error("Unexpected error")
        raise e
