import boto3
from botocore.exceptions import ClientError
from common import body_json, clean_bucket, response, aws_error


def lambda_handler(event, context):
    try:
        bucket = clean_bucket(body_json(event).get("bucket"))
        # Este taller se despliega en us-east-1; no se debe enviar LocationConstraint.
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=bucket)
        return response(201, {"mensaje": "Bucket creado", "bucket": bucket, "region": "us-east-1"})
    except ValueError as exc:
        return response(400, {"error": str(exc)})
    except ClientError as exc:
        return aws_error(exc)
