resource "aws_dynamodb_table" "students" {
  name         = "${var.project_name}-${var.environment}-students"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"

  attribute {
    name = "email"
    type = "S"
  }

  deletion_protection_enabled = false

  tags = {
    Name        = "${var.project_name}-${var.environment}-students"
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
