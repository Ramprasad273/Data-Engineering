# Security Policy

## Security Architecture & Best Practices

This document outlines security configurations, risks, and hardening requirements for the projects in this repository.

> [!WARNING]
> The default configurations provided in this repository are intended exclusively for **local development, sandbox testing, and educational validation**.
>
> Services are provisioned with local default credentials for ease of testing. Do not expose these configurations to public networks or deploy them to production environments without completing the security hardening outlined below.

## Development vs Production Standards

### Local Development Environment
- Scope: Single-node local execution, automated CI tests, architectural validation.
- Access: Bound to localhost or private Docker bridge network (`airflow_network`).
- Credentials: Default local parameters for zero-configuration startup.
- Data: Synthetic datasets only. No Protected Health Information (PHI) or Personally Identifiable Information (PII).

### Production Hardening Requirements
- Credential Security: No hardcoded values. All secrets injected via KMS, HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets.
- Encryption: Mandatory TLS 1.3 in-transit encryption across all endpoints (Airflow webserver, PostgreSQL warehouse, Spark internal RPC, Grafana). Encryption-at-rest enabled for all storage volumes.
- Network Isolation: Databases and compute workers located within isolated private subnets with strictly defined egress/ingress security groups.
- Authentication & Authorization: Role-Based Access Control (RBAC) enforced across Airflow DAG execution, warehouse schemas, and dashboard viewers. Integration with OpenID Connect (OIDC), OAuth 2.0, or SAML IdP.
- Auditing: Centralized audit logging of query histories, user authentications, and pipeline execution logs.

## Credential Management

### Authentication Environment Variables

Authentication parameters are driven dynamically through environment variables and must never be committed to version control:

| Service | Username Variable | Password Variable | Scope |
|---------|-------------------|-------------------|-------|
| Airflow Webserver | `_AIRFLOW_WWW_USER_USERNAME` | `_AIRFLOW_WWW_USER_PASSWORD` | Airflow Web UI & API |
| Grafana Server | `GF_SECURITY_ADMIN_USER` | `GF_SECURITY_ADMIN_PASSWORD` | Grafana Admin Access |
| Airflow Metadata DB | `POSTGRES_USER` | `POSTGRES_PASSWORD` | Airflow Internal Metadata |
| Clinical Data Warehouse | `CLINICAL_DB_USER` | `CLINICAL_DB_PASSWORD` | Healthcare Data Warehouse |

### Overriding Credentials Locally

1. Copy the environment template:
   ```bash
   cp de_projects/airflow_sandbox/.env.example de_projects/airflow_sandbox/.env
   ```

2. Generate cryptographically strong random passwords:
   ```bash
   openssl rand -base64 32
   ```

3. Populate `.env` with your secure credentials. The `.env` file is excluded from Git tracking via `.gitignore`.

4. Start the stack with the overridden environment file:
   ```bash
   docker-compose --env-file .env up -d
   ```

## Network & Service Isolation

1. **Private Docker Bridge**: All inter-service communication (Airflow -> Metadata DB, Airflow -> Clinical DB, Prometheus -> Exporters) occurs across an internal bridge network (`airflow_network`).
2. **Port Exposure**: In production configurations, bind ports to `127.0.0.1` or eliminate host port bindings entirely when fronted by an API Gateway or Ingress Controller:
   ```yaml
   ports:
     - "127.0.0.1:8080:8080"
   ```
3. **Database Safeguards**: The PostgreSQL warehouse enforces connection limits and role-based permissions to isolate staging ingestion from marts consumption.

## Static Analysis & Security Scanning

To maintain platform integrity, the following security checks should be incorporated into the CI/CD pipeline:

1. **Dependency Vulnerability Scanning**:
   ```bash
   pip-audit --requirement requirements.txt
   ```

2. **Container Image Scanning**:
   ```bash
   trivy image apache/airflow:2.9.3
   ```

3. **Static Application Security Testing (SAST)**:
   ```bash
   bandit -r de_projects/airflow_sandbox/dags/
   ```

4. **Secret Detection**:
   Scan commits for accidental secret commits using `gitleaks` or `detect-secrets`.

## Vulnerability Reporting

If you discover a potential security vulnerability or misconfiguration within this repository:

1. Do not report security issues via public GitHub issues or discussions.
2. Submit a private security advisory through the GitHub repository's **Security** tab (`Security` > `Advisories` > `Report a vulnerability`).
3. Include detailed steps to reproduce, an assessment of potential impact, and suggested remediations if available.
