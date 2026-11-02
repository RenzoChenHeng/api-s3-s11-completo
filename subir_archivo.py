import base64
import binascii
import boto3
from botocore.exceptions import ClientError
from common import body_json, clean_bucket, clean_dir, response, aws_error


def lambda_handler(event, context):
    try:
        data = body_json(event)
        bucket = clean_bucket(data.get("bucket"))
        prefix = clean_dir(data.get("directorio"))
        archivo = data.get("archivo")
        if not isinstance(archivo, str) or not archivo.strip() or archivo.strip() in (".", "..") or "/" in archivo or "\\" in archivo:
            raise ValueError("Indique un nombre de archivo sin rutas, por ejemplo prueba.txt")
        archivo = archivo.strip()
        if "contenido_base64" in data:
            if not isinstance(data["contenido_base64"], str):
                raise ValueError("contenido_base64 debe ser texto")
            try:
                contenido = base64.b64decode(data["contenido_base64"], validate=True)
            except (binascii.Error, ValueError) as exc:
                raise ValueError("El contenido_base64 no es valido") from exc
        elif "contenido" in data and isinstance(data["contenido"], str):
            contenido = data["contenido"].encode("utf-8")
        else:
            raise ValueError("Envia contenido o contenido_base64 en el JSON")
        if len(contenido) > 1024 * 1024:
            raise ValueError("Para este taller el archivo no debe superar 1 MiB")
        key = prefix + archivo
        boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=contenido)
        return response(201, {"mensaje": "Archivo subido", "bucket": bucket, "key": key, "bytes": len(contenido)})
    except ValueError as exc:
        return response(400, {"error": str(exc)})
    except ClientError as exc:
        return aws_error(exc)
