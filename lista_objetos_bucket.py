import boto3
from botocore.exceptions import ClientError
from common import body_json, clean_bucket, response, aws_error


def lambda_handler(event, context):
    try:
        bucket = clean_bucket(body_json(event).get("bucket"))
        s3 = boto3.client("s3")
        names = []
        token = None
        while True:
            params = {"Bucket": bucket}
            if token:
                params["ContinuationToken"] = token
            result = s3.list_objects_v2(**params)
            names.extend(obj["Key"] for obj in result.get("Contents", []))
            if not result.get("IsTruncated"):
                break
            token = result["NextContinuationToken"]
        return response(200, {"bucket": bucket, "lista_objetos": names})
    except ValueError as exc:
        return response(400, {"error": str(exc)})
    except ClientError as exc:
        return aws_error(exc)
