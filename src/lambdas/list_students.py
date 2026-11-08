import base64
import binascii
import json
import logging
import os
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ.get("STUDENTS_TABLE_NAME")
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME) if TABLE_NAME else None


def json_serializer(value):
    """Convert DynamoDB Decimal values into JSON-compatible numbers."""
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)

    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def response(status_code, payload):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload, default=json_serializer),
    }


def encode_next_token(last_evaluated_key):
    """Encode DynamoDB's LastEvaluatedKey for the next request."""
    if not last_evaluated_key:
        return None

    token_data = json.dumps(
        last_evaluated_key,
        default=json_serializer,
    ).encode("utf-8")

    return base64.urlsafe_b64encode(token_data).decode("utf-8").rstrip("=")


def decode_next_token(token):
    """Decode a pagination token into DynamoDB's ExclusiveStartKey."""
    if not isinstance(token, str) or not token:
        raise ValueError("Invalid pagination token")

    padded_token = token + "=" * (-len(token) % 4)

    decoded_token = base64.b64decode(
        padded_token,
        altchars=b"-_",
        validate=True,
    )

    last_evaluated_key = json.loads(decoded_token.decode("utf-8"))

    if (
        not isinstance(last_evaluated_key, dict)
        or not last_evaluated_key
        or not isinstance(last_evaluated_key.get("email"), str)
        or not last_evaluated_key["email"]
    ):
        raise ValueError("Invalid pagination token")

    return last_evaluated_key


def lambda_handler(event, context):
    """Return a paginated list of registered students."""
    if table is None:
        logger.error("STUDENTS_TABLE_NAME environment variable is not configured")
        return response(500, {"message": "Server configuration error"})

    query_parameters = event.get("queryStringParameters") or {}

    if not isinstance(query_parameters, dict):
        return response(400, {"message": "Invalid query parameters"})

    limit_value = query_parameters.get("limit", DEFAULT_PAGE_SIZE)

    try:
        limit = int(limit_value)
    except (TypeError, ValueError):
        return response(400, {"message": "Limit must be an integer"})

    if not 1 <= limit <= MAX_PAGE_SIZE:
        return response(
            400,
            {"message": f"Limit must be between 1 and {MAX_PAGE_SIZE}"},
        )

    scan_parameters = {"Limit": limit}

    next_token = query_parameters.get("nextToken")

    if next_token is not None:
        try:
            scan_parameters["ExclusiveStartKey"] = decode_next_token(next_token)
        except (
            ValueError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            binascii.Error,
        ):
            return response(
                400,
                {"message": "Invalid pagination token"},
            )

    try:
        scan_result = table.scan(**scan_parameters)

        students = scan_result.get("Items", [])
        last_evaluated_key = scan_result.get("LastEvaluatedKey")

        continuation_token = encode_next_token(last_evaluated_key)

        logger.info(
            "Student listing request completed successfully. Records returned: %s",
            len(students),
        )

        return response(
            200,
            {
                "students": students,
                "nextToken": continuation_token,
            },
        )

    except ClientError:
        logger.exception("DynamoDB error while retrieving students")
        return response(
            500,
            {"message": "Unable to retrieve student records"},
        )

    except Exception:
        logger.exception("Unexpected error while retrieving students")
        return response(
            500,
            {"message": "An unexpected error occurred"},
        )
