
# Package signup Lambda source code
data "archive_file" "signup" {
  type        = "zip"
  source_file = "${path.module}/../src/lambdas/signup_students.py"
  output_path = "${path.module}/build/signup_students.zip"
}

# Package list Lambda source code
data "archive_file" "list" {
  type        = "zip"
  source_file = "${path.module}/../src/lambdas/list_students.py"
  output_path = "${path.module}/build/list_students.zip"
}

# Signup Lambda function
resource "aws_lambda_function" "signup_students" {
  function_name = "${var.project_name}-${var.environment}-signup"
  role          = aws_iam_role.signup_lambda.arn

  filename         = data.archive_file.signup.output_path
  source_code_hash = data.archive_file.signup.output_base64sha256

  handler       = "signup_students.lambda_handler"
  runtime       = "python3.12"
  architectures = ["x86_64"]

  timeout     = 10
  memory_size = 128

  environment {
    variables = {
      STUDENTS_TABLE_NAME = aws_dynamodb_table.students.name
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  depends_on = [
    aws_iam_role_policy_attachment.signup_logging,
    aws_iam_role_policy.signup_dynamodb
  ]
}

# List Lambda function
resource "aws_lambda_function" "list_students" {
  function_name = "${var.project_name}-${var.environment}-list"
  role          = aws_iam_role.list_lambda.arn

  filename         = data.archive_file.list.output_path
  source_code_hash = data.archive_file.list.output_base64sha256

  handler       = "list_students.lambda_handler"
  runtime       = "python3.12"
  architectures = ["x86_64"]

  timeout     = 10
  memory_size = 128

  environment {
    variables = {
      STUDENTS_TABLE_NAME = aws_dynamodb_table.students.name
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  depends_on = [
    aws_iam_role_policy_attachment.list_logging,
    aws_iam_role_policy.list_dynamodb
  ]
}

# Signup Lambda log group
resource "aws_cloudwatch_log_group" "signup" {
  name              = "/aws/lambda/${aws_lambda_function.signup_students.function_name}"
  retention_in_days = 7

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# List Lambda log group
resource "aws_cloudwatch_log_group" "list" {
  name              = "/aws/lambda/${aws_lambda_function.list_students.function_name}"
  retention_in_days = 7

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

