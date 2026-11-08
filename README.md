# Student Registration Serverless DevOps Project

A hands-on, production-oriented DevOps project that modernizes a student registration application and demonstrates end-to-end AWS cloud engineering, Infrastructure as Code, CI/CD, security automation, containerization, monitoring, logging, and observability.

The project uses an AWS serverless architecture as its foundation and progressively introduces industry-standard DevOps tools and practices.

## 1. Project Objectives

- Modernize and secure an existing Python-based serverless application.
- Build repeatable AWS infrastructure using Terraform.
- Implement automated CI/CD with Jenkins and GitHub.
- Apply DevSecOps practices throughout the development lifecycle.
- Secure application credentials and integration tokens using AWS Secrets Manager.
- Implement centralized logging, monitoring, alerting, and distributed tracing.
- Explore Prometheus, Grafana, and Loki for metrics visualization and log aggregation.
- Develop practical skills that demonstrate real-world Cloud, DevOps, and SRE engineering capabilities.

## 2. Application Architecture

The application is a student registration portal.

The initial architecture consists of:

- Frontend: HTML, Bootstrap, JavaScript, hosted on an EC2 instance running Apache.
- API: Amazon API Gateway.
- Compute: AWS Lambda functions written in Python.
- Database: Amazon DynamoDB.

The architecture will be progressively improved, including evaluating S3 and CloudFront for serverless frontend hosting.

## 3. Technology Stack

### Cloud Infrastructure and AWS Services

| Technology | Purpose |
|---|---|
| AWS | Primary cloud platform |
| Amazon API Gateway | Application API endpoints |
| AWS Lambda | Serverless application compute |
| Amazon DynamoDB | Student registration database |
| Amazon EC2 | Initial frontend hosting |
| Amazon S3 | Static assets, deployment artifacts and backups where appropriate |
| Amazon CloudFront | CDN and frontend delivery |
| AWS IAM | Identity and access management |
| AWS Secrets Manager | Secure storage and retrieval of application secrets and integration credentials |
| AWS KMS | Encryption key management |
| Amazon CloudWatch | Application logs, metrics, dashboards and alarms |
| AWS CloudTrail | API activity and auditing |
| AWS X-Ray / OpenTelemetry | Distributed tracing and application observability |

### Infrastructure as Code

| Technology | Purpose |
|---|---|
| Terraform | Provision and manage AWS infrastructure |
| Terraform modules | Reusable infrastructure components |
| TFLint | Terraform configuration linting |
| Checkov | Infrastructure as Code security scanning |

Terraform will own the foundational AWS infrastructure. Application deployment resources will have a clearly defined ownership boundary to avoid multiple tools managing the same resources.

### Programming and Application Development

| Technology | Purpose |
|---|---|
| Python | Lambda application development |
| Boto3 | AWS SDK for Python |
| HTML / CSS / Bootstrap | Frontend development |
| JavaScript | Frontend API integration |
| JSON | API communication and configuration |

### CI/CD and Version Control

| Technology | Purpose |
|---|---|
| Git | Source code version control |
| GitHub | Source code repository and pull requests |
| Jenkins | CI/CD automation |
| GitHub Webhooks | Trigger pipeline execution |
| Jenkins Pipeline | Automated build, test, security scan and deployment |
| AWS IAM federation / GitHub OIDC | Short-lived AWS credentials for CI/CD where supported |

### Testing and Code Quality

| Technology | Purpose |
|---|---|
| Pytest | Automated Python testing |
| Moto | Mock AWS services during unit tests |
| Ruff | Python linting and formatting |
| Bandit | Python security analysis |
| Boto3 Stubber | Mock AWS SDK responses where useful |
| Integration tests | Validate interactions with deployed AWS services |

### Containerization and Kubernetes Learning

| Technology | Purpose |
|---|---|
| Docker | Container fundamentals, packaging and local development tooling |
| Docker Compose | Local multi-service development where useful |
| Trivy | Container image and dependency vulnerability scanning |
| Kubernetes / kind | Optional local Kubernetes learning environment |
| Helm | Optional Kubernetes application packaging |

The core application is serverless and does not require Kubernetes. Kubernetes and Helm will be treated as an optional learning extension rather than mandatory components of the application architecture.

### Monitoring, Logging and Observability

| Technology | Purpose |
|---|---|
| Amazon CloudWatch | Native AWS metrics, logs, dashboards and alarms |
| Prometheus | Metrics collection and monitoring concepts |
| Grafana | Metrics visualization and dashboards |
| Loki | Centralized log aggregation |
| Grafana Alloy | Log and telemetry collection and forwarding |
| Alertmanager | Prometheus alert routing and notification management |
| OpenTelemetry | Standardized telemetry instrumentation |
| AWS X-Ray | Distributed tracing for AWS application components |
| Slack | Operational alerts and deployment notifications |

CloudWatch will be the initial monitoring and logging foundation. Prometheus, Grafana and Loki will be introduced as additional observability capabilities where technically appropriate.

For serverless workloads, we'll evaluate Amazon Managed Service for Prometheus and Amazon Managed Grafana or a cost-conscious self-managed alternative before selecting an implementation.

### DevSecOps and Security

| Technology | Purpose |
|---|---|
| AWS Secrets Manager | Secure runtime secrets and integration credentials |
| AWS KMS | Encryption |
| AWS IAM | Least-privilege access controls |
| AWS CloudTrail | Auditing |
| Bandit | Python security scanning |
| Checkov | Terraform security scanning |
| Trivy | Dependency and container vulnerability scanning |
| Gitleaks | Detect secrets accidentally committed to Git |
| Dependency scanning | Identify vulnerable application libraries |
| Branch protection | Protect the main GitHub branch |
| Pull request reviews | Enforce controlled code changes |

Secrets must never be committed to GitHub, embedded in application packages, exposed in CI/CD logs, or stored as plaintext in configuration files.

Lambda functions should use narrowly scoped execution roles. Jenkins should use short-lived AWS credentials rather than permanent access keys wherever practical.

## 4. Target Architecture and DevOps Workflow

The intended workflow is:

1. Developers make changes in feature branches.
2. Changes are pushed to GitHub.
3. A pull request is opened against `main`.
4. GitHub triggers Jenkins through a webhook.
5. Jenkins runs automated tests and code-quality checks.
6. Security scanning checks the application and Terraform configuration.
7. Approved changes are merged into `main`.
8. Jenkins deploys the application and infrastructure changes through controlled stages.
9. AWS services run the application.
10. CloudWatch and additional observability tools collect operational telemetry.
11. Alerts are delivered through Slack.

## 5. AWS Security and Secrets Management

AWS Secrets Manager will be used for genuine application and integration secrets, including:

- Slack incoming webhook URLs.
- Third-party API credentials when required.
- Other runtime integration credentials as the application evolves.

The project will demonstrate:

- IAM least privilege.
- KMS encryption.
- Secrets Manager access policies.
- Secure runtime secret retrieval.
- Secret rotation considerations.
- CloudTrail auditing.
- Secure CI/CD authentication.
- Separation of application, infrastructure and deployment permissions.

AWS access keys will not be hardcoded into application code or committed to the repository.

## 6. Implementation Roadmap

| Phase | Deliverable |
|---|---|
| 1 | Repository setup and project organization |
| 2 | Python application refactoring and improvements |
| 3 | Unit testing and code quality automation |
| 4 | Frontend and API improvements |
| 5 | Terraform infrastructure implementation |
| 6 | AWS deployment and application validation |
| 7 | AWS Secrets Manager and security implementation |
| 8 | Jenkins and GitHub CI/CD pipeline |
| 9 | DevSecOps and automated security scanning |
| 10 | CloudWatch monitoring, logging and alerting |
| 11 | Prometheus, Grafana and Loki observability integration |
| 12 | Slack notifications and operational automation |
| 13 | Reliability, backup, recovery and production-readiness improvements |
| 14 | Optional Docker, Kubernetes and Helm learning extension |

## 7. Development Environment

Initial development environment:

- OS: Ubuntu 24.04 LTS on WSL2.
- Cloud provider: AWS.
- AWS Region: us-east-2 (Ohio).
- Programming language: Python.
- Source control: Git and GitHub.
- Infrastructure as Code: Terraform.

## 8. Project Principles

- Build incrementally and validate every stage.
- Use reusable and maintainable infrastructure code.
- Apply least-privilege security principles.
- Automate repetitive tasks.
- Keep secrets out of source control.
- Separate development and production configurations.
- Monitor application health and infrastructure performance.
- Keep infrastructure costs under control.
- Document implementation decisions and troubleshooting.
- Use Git commits and pull requests to demonstrate engineering discipline.

## 9. Project Status

**Current status:** Initial repository created. Application modernization and development environment setup in progress.

This is an evolving hands-on project. Technologies listed in the roadmap represent intended learning and implementation areas; they should not be interpreted as already deployed or configured.
