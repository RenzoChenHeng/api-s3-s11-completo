import boto3
from botocore.exceptions import ClientError
from common import body_json, clean_bucket, clean_dir, response, aws_error


def lambda_handler(event, context):
    try:
        data = body_json(event)
        bucket = clean_bucket(data.get("bucket"))
        prefix = clean_dir(data.get("directorio"))
        # En S3 un directorio se representa con un objeto vacio cuyo Key termina en /.
        boto3.client("s3").put_object(Bucket=bucket, Key=prefix, Body=b"")
        return response(201, {"mensaje": "Directorio creado", "bucket": bucket, "directorio": prefix})
    except ValueError as exc:
        return response(400, {"error": str(exc)})
    except ClientError as exc:
        return aws_error(exc)
