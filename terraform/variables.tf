variable "aws_region" {
  description = "AWS region for Student Registration infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the Student Registration project"
  type        = string
  default     = "student-registration"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
variable "cognito_domain_prefix" {
  description = "Globally unique Cognito hosted UI domain prefix"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$", var.cognito_domain_prefix))
    error_message = "Use lowercase letters, numbers, and hyphens. The prefix cannot start or end with a hyphen."
  }
}

variable "cognito_callback_url" {
  description = "Frontend URL Cognito redirects to after authentication"
  type        = string
  default     = "http://localhost:8084/"
}

variable "cognito_logout_url" {
  description = "Frontend URL Cognito redirects to after logout"
  type        = string
  default     = "http://localhost:8084/"
}
variable "frontend_origin" {
  description = "Browser origin allowed to call the API"
  type        = string
  default     = "http://localhost:8084"
}
