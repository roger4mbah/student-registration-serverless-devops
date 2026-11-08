import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

# Configure application logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Read configuration from Lambda environment variables
TABLE_NAME = os.environ.get("STUDENTS_TABLE_NAME")

# Initialize DynamoDB resources outside the handler.
# Lambda can reuse these objects across warm invocations.
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME) if TABLE_NAME else None


def response(status_code, message):
    """Return a consistent API Gateway HTTP response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message}),
    }


def lambda_handler(event, context):
    """Register a student in DynamoDB."""

    # Ensure the required database configuration exists.
    if table is None:
        logger.error("STUDENTS_TABLE_NAME environment variable is not configured")
        return response(500, "Server configuration error")

    # Validate that the request contains a body.
    request_body = event.get("body")

    if not request_body:
        return response(400, "Request body is required")

    # Parse JSON request body.
    try:
        body = json.loads(request_body)
    except (json.JSONDecodeError, TypeError):
        return response(400, "Request body must contain valid JSON")

    # Ensure the JSON body is an object.
    if not isinstance(body, dict):
        return response(400, "Request body must be a JSON object")

    # Validate required fields.
    required_fields = ["name", "age", "email", "country"]

    missing_fields = [
        field
        for field in required_fields
        if field not in body or body[field] is None or body[field] == ""
    ]

    if missing_fields:
        return response(
            400, f"Missing or empty required fields: {', '.join(missing_fields)}"
        )

    # Extract and validate student information.
    name = body["name"]
    age = body["age"]
    email = body["email"]
    country = body["country"]

    if not all(
        isinstance(value, str) and value.strip() for value in [name, email, country]
    ):
        return response(400, "Name, email, and country must be non-empty strings")

    name = name.strip()
    email = email.strip().lower()
    country = country.strip()

    if isinstance(age, bool) or not isinstance(age, int) or not 1 <= age <= 120:
        return response(400, "Age must be an integer between 1 and 120")

    if "@" not in email or email.startswith("@") or email.endswith("@"):
        return response(400, "A valid email address is required")

    # Save the student, but only if the email does not already exist.
    try:
        table.put_item(
            Item={"email": email, "name": name, "age": age, "country": country},
            ConditionExpression="attribute_not_exists(email)",
        )

        logger.info("Student registration created successfully")
        return response(201, "Student signed up successfully")

    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code")

        if error_code == "ConditionalCheckFailedException":
            return response(409, "A student with this email is already registered")

        logger.exception("DynamoDB error during student registration")
        return response(500, "Unable to complete student registration")

    except Exception:
        logger.exception("Unexpected error during student registration")
        return response(500, "An unexpected error occurred")
