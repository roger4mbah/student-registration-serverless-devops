# Lambda execution role trust policy
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type = "Service"

      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

# Signup Lambda execution role
resource "aws_iam_role" "signup_lambda" {
  name               = "${var.project_name}-${var.environment}-signup-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# List Lambda execution role
resource "aws_iam_role" "list_lambda" {
  name               = "${var.project_name}-${var.environment}-list-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Basic CloudWatch logging permissions for signup Lambda
resource "aws_iam_role_policy_attachment" "signup_logging" {
  role       = aws_iam_role.signup_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Basic CloudWatch logging permissions for list Lambda
resource "aws_iam_role_policy_attachment" "list_logging" {
  role       = aws_iam_role.list_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Allow signup Lambda to insert student records
resource "aws_iam_role_policy" "signup_dynamodb" {
  name = "students-put-item"
  role = aws_iam_role.signup_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "dynamodb:PutItem"
        ]

        Resource = aws_dynamodb_table.students.arn
      }
    ]
  })
}

# Allow list Lambda to retrieve student records
resource "aws_iam_role_policy" "list_dynamodb" {
  name = "students-scan"
  role = aws_iam_role.list_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "dynamodb:Scan"
        ]

        Resource = aws_dynamodb_table.students.arn
      }
    ]
  })
}
