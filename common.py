import json
import re
from botocore.exceptions import ClientError


def body_json(event):
    payload = event.get("body", {}) or {}
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ValueError("Body debe contener JSON valido") from exc
    if not isinstance(payload, dict):
        raise ValueError("Body debe ser un objeto JSON")
    return payload


def response(status, data):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json; charset=utf-8", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(data, ensure_ascii=False),
    }


def clean_bucket(value):
    if not isinstance(value, str):
        raise ValueError("Debe indicar bucket como texto")
    name = value.strip()
    if not (3 <= len(name) <= 63) or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*[a-z0-9]", name):
        raise ValueError("Nombre de bucket invalido: use 3-63 caracteres, minusculas, numeros, guiones y puntos")
    if ".." in name or ".-" in name or "-." in name or re.fullmatch(r"\d+\.\d+\.\d+\.\d+", name):
        raise ValueError("Nombre de bucket invalido")
    return name


def clean_dir(value):
    if not isinstance(value, str):
        raise ValueError("El directorio debe ser texto")
    path = value.strip().strip("/")
    if not path or any(part in (".", "..") for part in path.split("/")):
        raise ValueError("Directorio invalido")
    return path + "/"


def aws_error(exc):
    code = exc.response.get("Error", {}).get("Code", "ErrorAWS")
    status = 403 if code in ("AccessDenied", "AllAccessDisabled") else 404 if code in ("NoSuchBucket", "404") else 409 if code in ("BucketAlreadyExists", "BucketAlreadyOwnedByYou") else 500
    return response(status, {"error": code, "mensaje": "AWS S3 rechazo la operacion; revise permisos, region y nombres"})
