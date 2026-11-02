import boto3
from botocore.exceptions import ClientError
from common import response, aws_error


def lambda_handler(event, context):
    try:
        s3 = boto3.client("s3")
        nombres = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
        return response(200, {"lista_buckets": nombres})
    except ClientError as exc:
        return aws_error(exc)
