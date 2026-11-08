import importlib.util
import json
from pathlib import Path

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_aws


def load_list_students_module(module_name):
    """Load the Lambda module from its source file."""
    project_root = Path(__file__).resolve().parents[1]
    module_path = project_root / "src" / "lambdas" / "list_students.py"

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


@pytest.fixture
def students_module(monkeypatch):
    """Create a simulated DynamoDB table for each test."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("STUDENTS_TABLE_NAME", "Students")

    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        table = dynamodb.create_table(
            TableName="Students",
            KeySchema=[
                {"AttributeName": "email", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "email", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        module = load_list_students_module("list_students_under_test")

        yield module, table


def test_list_students_success(students_module):
    module, table = students_module

    table.put_item(
        Item={
            "email": "alice@example.com",
            "name": "Alice",
            "age": 25,
            "country": "USA",
        }
    )
    table.put_item(
        Item={
            "email": "bob@example.com",
            "name": "Bob",
            "age": 30,
            "country": "Canada",
        }
    )

    result = module.lambda_handler(
        {"queryStringParameters": None},
        None,
    )

    payload = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert len(payload["students"]) == 2
    assert payload["nextToken"] is None


def test_list_students_empty_table(students_module):
    module, _table = students_module

    result = module.lambda_handler(
        {"queryStringParameters": None},
        None,
    )

    payload = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert payload["students"] == []
    assert payload["nextToken"] is None


def test_list_students_pagination(students_module):
    module, table = students_module

    for number in range(3):
        table.put_item(
            Item={
                "email": f"student{number}@example.com",
                "name": f"Student {number}",
                "age": 20 + number,
                "country": "USA",
            }
        )

    first_result = module.lambda_handler(
        {"queryStringParameters": {"limit": "2"}},
        None,
    )

    first_payload = json.loads(first_result["body"])

    assert first_result["statusCode"] == 200
    assert len(first_payload["students"]) == 2
    assert first_payload["nextToken"] is not None

    second_result = module.lambda_handler(
        {
            "queryStringParameters": {
                "limit": "2",
                "nextToken": first_payload["nextToken"],
            }
        },
        None,
    )

    second_payload = json.loads(second_result["body"])

    assert second_result["statusCode"] == 200
    assert len(second_payload["students"]) == 1
    assert second_payload["nextToken"] is None

    all_emails = {
        student["email"]
        for student in first_payload["students"] + second_payload["students"]
    }

    assert len(all_emails) == 3


@pytest.mark.parametrize("limit", ["abc", "0", "51"])
def test_list_students_invalid_limit(students_module, limit):
    module, _table = students_module

    result = module.lambda_handler(
        {"queryStringParameters": {"limit": limit}},
        None,
    )

    assert result["statusCode"] == 400


def test_list_students_invalid_pagination_token(students_module):
    module, _table = students_module

    result = module.lambda_handler(
        {"queryStringParameters": {"nextToken": "not-a-valid-token"}},
        None,
    )

    assert result["statusCode"] == 400


def test_list_students_missing_table_configuration(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.delenv("STUDENTS_TABLE_NAME", raising=False)

    with mock_aws():
        module = load_list_students_module("list_students_missing_config")

        result = module.lambda_handler(
            {"queryStringParameters": None},
            None,
        )

    assert result["statusCode"] == 500
    assert json.loads(result["body"])["message"] == "Server configuration error"


def test_list_students_dynamodb_error(students_module, monkeypatch):
    module, _table = students_module

    def raise_dynamodb_error(**kwargs):
        raise ClientError(
            {
                "Error": {
                    "Code": "AccessDeniedException",
                    "Message": "Access denied",
                }
            },
            "Scan",
        )

    monkeypatch.setattr(module.table, "scan", raise_dynamodb_error)
    result = module.lambda_handler(
        {"queryStringParameters": None},
        None,
    )

    assert result["statusCode"] == 500
    assert json.loads(result["body"])["message"] == "Unable to retrieve student records"
