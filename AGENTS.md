
# Project Instructions for Codex

## Project Overview
This is a hands-on DevOps portfolio project:
student-registration-serverless-devops.

Environment:
- Ubuntu 24.04 running under WSL2
- Docker Desktop
- Kubernetes using kind
- Helm
- AWS Lambda and DynamoDB
- Terraform
- GitHub Actions
- Jenkins (planned integration)
- Prometheus and Grafana (planned observability)

## Learning Requirements
- I am learning DevOps through this project.
- Explain what each change accomplishes and why.
- Work incrementally, one logical task at a time.
- Provide exact file paths and commands.
- Explain expected command output.
- Do not make large batches of changes without explaining them.
- Prefer simple, maintainable, production-minded solutions.

## AWS Safety Rules
- Never run terraform apply or terraform destroy without my explicit approval.
- Never provision, modify, or delete AWS resources without my explicit approval.
- Never run AWS CLI commands that modify resources without approval.
- Explain potential AWS costs before proposing deployment.
- Preserve existing Lambda functions, DynamoDB tables and records, IAM resources, and CloudWatch log groups.
- Do not introduce expensive infrastructure without discussing alternatives.

## Local Environment Safety
- Do not delete the existing kind cluster.
- Do not stop or remove existing Docker containers.
- Do not delete Kubernetes deployments, services, pods, or Helm releases without approval.
- Preserve existing Jenkins and other local services.
- Ask before changing local infrastructure.

## Terraform and Git Safety
- Never delete or overwrite Terraform state files.
- Never commit terraform.tfstate, terraform.tfstate.backup, secrets, credentials, or generated build artifacts.
- Review .gitignore before staging Terraform files.
- Do not expose secrets in terminal output or logs.
- Preserve existing infrastructure definitions and resources.

## Development Standards
- Use Terraform for AWS infrastructure.
- Use Python for Lambda functions.
- Use Docker for containerization.
- Use Helm for Kubernetes application deployment.
- Use GitHub Actions and Jenkins for CI/CD.
- Use Trivy for container security scanning.
- Use Prometheus and Grafana for observability.
- Follow least-privilege IAM principles.
- Include tests, validation, and security checks where appropriate.

## Working Rules
- Inspect before modifying.
- Explain the proposed changes before implementing significant changes.
- Show which files will be modified.
- Review diffs after modifications.
- Run relevant local validation and tests.
- Never claim a task succeeded without verifying its output.
- Wait for my approval before destructive or AWS-changing operations.

