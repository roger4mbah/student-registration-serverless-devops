import importlib.util
import json
from pathlib import Path

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_aws


@pytest.fixture
def lambda_module(monkeypatch):
    """Create an isolated mock DynamoDB table for each test."""

    # Configure dummy AWS credentials and local test settings.
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-2")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("STUDENTS_TABLE_NAME", "Students")

    with mock_aws():
        # Locate the Lambda source file.
        lambda_path = (
            Path(__file__).resolve().parents[1]
            / "src"
            / "lambdas"
            / "signup_students.py"
        )

        # Load the Lambda module.
        spec = importlib.util.spec_from_file_location("signup_students", lambda_path)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Create the mocked DynamoDB table.
        dynamodb = boto3.resource("dynamodb", region_name="us-east-2")

        dynamodb.create_table(
            TableName="Students",
            KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        yield module


def make_event(body):
    """Build an API Gateway-style request event."""
    return {"body": body}


def test_successful_student_registration(lambda_module):
    """A valid student should be registered successfully."""

    student = {
        "name": "John Doe",
        "age": 20,
        "email": "john@example.com",
        "country": "USA",
    }

    result = lambda_module.lambda_handler(make_event(json.dumps(student)), None)

    assert result["statusCode"] == 201

    # Verify that the student was actually saved in DynamoDB.
    saved_student = lambda_module.table.get_item(Key={"email": "john@example.com"})

    assert saved_student["Item"]["name"] == "John Doe"
    assert saved_student["Item"]["age"] == 20


def test_missing_required_field(lambda_module):
    """A request without a required field should be rejected."""

    student = {
        "name": "John Doe",
        "age": 20,
        "email": "john@example.com",
    }

    result = lambda_module.lambda_handler(make_event(json.dumps(student)), None)

    assert result["statusCode"] == 400


def test_invalid_json(lambda_module):
    """Malformed JSON should return HTTP 400."""

    result = lambda_module.lambda_handler(make_event("{invalid-json"), None)

    assert result["statusCode"] == 400


def test_invalid_age(lambda_module):
    """Age must be an integer between 1 and 120."""

    student = {
        "name": "John Doe",
        "age": 150,
        "email": "john@example.com",
        "country": "USA",
    }

    result = lambda_module.lambda_handler(make_event(json.dumps(student)), None)

    assert result["statusCode"] == 400


def test_duplicate_email_registration(lambda_module):
    """A second registration with the same email should be rejected."""

    student = {
        "name": "John Doe",
        "age": 20,
        "email": "john@example.com",
        "country": "USA",
    }

    first_result = lambda_module.lambda_handler(make_event(json.dumps(student)), None)

    second_student = {
        **student,
        "name": "Jane Doe",
    }

    second_result = lambda_module.lambda_handler(
        make_event(json.dumps(second_student)), None
    )

    assert first_result["statusCode"] == 201
    assert second_result["statusCode"] == 409

    # Confirm that the original record was not overwritten.
    saved_student = lambda_module.table.get_item(Key={"email": "john@example.com"})

    assert saved_student["Item"]["name"] == "John Doe"


def test_dynamodb_error(lambda_module, monkeypatch):
    """Unexpected DynamoDB errors should return HTTP 500."""

    student = {
        "name": "John Doe",
        "age": 20,
        "email": "john@example.com",
        "country": "USA",
    }

    def simulate_database_error(**kwargs):
        raise ClientError(
            {
                "Error": {
                    "Code": "InternalServerError",
                    "Message": "Simulated database failure",
                }
            },
            "PutItem",
        )

    monkeypatch.setattr(
        lambda_module.table,
        "put_item",
        simulate_database_error,
    )

    result = lambda_module.lambda_handler(make_event(json.dumps(student)), None)

    assert result["statusCode"] == 500
