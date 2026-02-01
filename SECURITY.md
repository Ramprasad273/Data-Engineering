# Security Policy

## 🔒 Security Best Practices

This document outlines security best practices for deploying and using the projects in this repository.

## ⚠️ Important Notice

> [!WARNING]
> **The projects in this repository are configured for LOCAL DEVELOPMENT and LEARNING purposes.**
> 
> They use default credentials and simplified security configurations to make it easy to get started. **NEVER deploy these configurations to production environments without proper security hardening.**

---

## 🛡️ Development vs Production

### Development Environment (This Repository)

**Purpose:** Learning, experimentation, local testing

**Security Level:** Basic (default credentials, no encryption)

**Acceptable Use:**
- ✅ Local development on your machine
- ✅ Learning and experimentation
- ✅ Testing and prototyping
- ✅ Educational purposes

**NOT Acceptable:**
- ❌ Production deployments
- ❌ Processing sensitive data
- ❌ Exposing to the internet
- ❌ Multi-user environments

### Production Environment

**Purpose:** Real-world data processing, business operations

**Security Level:** High (strong authentication, encryption, access control)

**Required Security Measures:**
- ✅ Strong, unique passwords
- ✅ Secrets management (Vault, AWS Secrets Manager, etc.)
- ✅ SSL/TLS encryption
- ✅ Network segmentation
- ✅ Role-based access control (RBAC)
- ✅ Audit logging
- ✅ Regular security updates
- ✅ Vulnerability scanning

---

## 🔑 Credential Management

### Default Credentials in This Repository

The following services use default credentials for development:

| Service | Default Username | Default Password | Environment Variable |
|---------|-----------------|------------------|---------------------|
| Airflow | admin | admin | `_AIRFLOW_WWW_USER_PASSWORD` |
| Grafana | admin | admin | `GF_SECURITY_ADMIN_PASSWORD` |
| PostgreSQL | airflow | airflow | `POSTGRES_PASSWORD` |

### How to Change Credentials

#### Option 1: Environment Variables (Recommended)

1. **Create a `.env` file** (never commit this!):
   ```bash
   # .env
   AIRFLOW_ADMIN_PASSWORD=your_secure_password_here
   GRAFANA_ADMIN_PASSWORD=your_secure_password_here
   POSTGRES_PASSWORD=your_secure_password_here
   ```

2. **Update docker-compose.yaml** to use environment variables:
   ```yaml
   environment:
     _AIRFLOW_WWW_USER_PASSWORD: ${AIRFLOW_ADMIN_PASSWORD}
     GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD}
     POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
   ```

3. **Load environment variables**:
   ```bash
   docker-compose --env-file .env up -d
   ```

#### Option 2: Docker Secrets

For production Docker Swarm deployments:

```yaml
secrets:
  airflow_password:
    external: true

services:
  airflow-webserver:
    secrets:
      - airflow_password
    environment:
      _AIRFLOW_WWW_USER_PASSWORD_FILE: /run/secrets/airflow_password
```

#### Option 3: External Secrets Management

Integrate with:
- **HashiCorp Vault**
- **AWS Secrets Manager**
- **Azure Key Vault**
- **Google Secret Manager**
- **Kubernetes Secrets**

---

## 🌐 Network Security

### Development

```yaml
# docker-compose.yaml
networks:
  internal:
    driver: bridge
    internal: true  # No external access
  
  external:
    driver: bridge
```

### Production

1. **Use Private Networks**
   - Place databases in private subnets
   - Use VPC/VNet isolation
   - Implement network policies

2. **Enable SSL/TLS**
   ```yaml
   # Airflow with SSL
   AIRFLOW__WEBSERVER__WEB_SERVER_SSL_CERT: /path/to/cert.pem
   AIRFLOW__WEBSERVER__WEB_SERVER_SSL_KEY: /path/to/key.pem
   ```

3. **Configure Firewalls**
   - Whitelist specific IPs
   - Block unnecessary ports
   - Use security groups

4. **Implement VPN/Bastion Hosts**
   - Access through VPN only
   - Use jump boxes for SSH
   - Implement zero-trust architecture

---

## 🔐 Authentication & Authorization

### Airflow

#### Enable RBAC

```python
# airflow.cfg
[webserver]
rbac = True
authenticate = True
auth_backend = airflow.contrib.auth.backends.password_auth
```

#### Configure OAuth/LDAP

```python
# For Google OAuth
[webserver]
auth_backend = airflow.contrib.auth.backends.google_auth

[google]
client_id = your_client_id
client_secret = your_client_secret
oauth_callback_route = /oauth2callback
domain = your_domain.com
```

### Grafana

#### Enable Authentication

```yaml
# grafana.ini
[auth]
disable_login_form = false

[auth.basic]
enabled = true

[auth.ldap]
enabled = true
config_file = /etc/grafana/ldap.toml
```

#### Configure SSO

```yaml
[auth.generic_oauth]
enabled = true
client_id = your_client_id
client_secret = your_client_secret
scopes = openid profile email
auth_url = https://your-idp.com/oauth/authorize
token_url = https://your-idp.com/oauth/token
```

### Prometheus

#### Enable Basic Auth

```yaml
# prometheus.yml
basic_auth_users:
  admin: $2y$10$hashed_password_here
```

---

## 📊 Monitoring Security

### Secure Prometheus

1. **Enable Authentication**
2. **Use HTTPS**
3. **Restrict Scrape Targets**
4. **Implement Network Policies**

### Secure Grafana

1. **Change Default Password**
2. **Enable HTTPS**
3. **Configure User Roles**
4. **Enable Audit Logging**
5. **Set Session Timeout**

```yaml
# grafana.ini
[security]
admin_password = ${GF_SECURITY_ADMIN_PASSWORD}
secret_key = ${GF_SECURITY_SECRET_KEY}
disable_gravatar = true

[auth]
disable_login_form = false
oauth_auto_login = false

[session]
session_life_time = 86400
cookie_secure = true
cookie_samesite = strict
```

---

## 🗄️ Database Security

### PostgreSQL

1. **Strong Passwords**
   ```sql
   ALTER USER airflow WITH PASSWORD 'strong_random_password';
   ```

2. **SSL Connections**
   ```yaml
   AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://user:pass@host:5432/db?sslmode=require
   ```

3. **Connection Limits**
   ```sql
   ALTER USER airflow CONNECTION LIMIT 50;
   ```

4. **Regular Backups**
   ```bash
   pg_dump -U airflow airflow > backup_$(date +%Y%m%d).sql
   ```

### Redis

1. **Require Password**
   ```yaml
   command: redis-server --requirepass your_password
   ```

2. **Bind to Localhost**
   ```yaml
   command: redis-server --bind 127.0.0.1
   ```

3. **Disable Dangerous Commands**
   ```yaml
   command: redis-server --rename-command FLUSHDB "" --rename-command FLUSHALL ""
   ```

---

## 🔍 Security Scanning

### Container Scanning

```bash
# Scan Docker images for vulnerabilities
docker scan airflow_sandbox_airflow-webserver:latest

# Use Trivy
trivy image airflow_sandbox_airflow-webserver:latest
```

### Dependency Scanning

```bash
# Python dependencies
pip-audit

# Or use safety
safety check
```

### Code Scanning

```bash
# Bandit for Python security issues
bandit -r ./dags/

# Semgrep
semgrep --config=auto ./
```

---

## 📝 Audit Logging

### Enable Airflow Audit Logs

```python
# airflow.cfg
[logging]
remote_logging = True
remote_base_log_folder = s3://your-bucket/airflow-logs
```

### Enable Grafana Audit Logs

```yaml
# grafana.ini
[log]
mode = console file
level = info

[log.file]
log_rotate = true
max_lines = 1000000
max_size_shift = 28
daily_rotate = true
max_days = 7
```

---

## 🚨 Incident Response

### Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: [security contact - add your email]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **24 hours:** Initial acknowledgment
- **7 days:** Assessment and plan
- **30 days:** Fix and disclosure (if applicable)

---

## ✅ Security Checklist

### Before Production Deployment

- [ ] Changed all default passwords
- [ ] Configured secrets management
- [ ] Enabled SSL/TLS
- [ ] Configured authentication (OAuth/LDAP)
- [ ] Enabled RBAC
- [ ] Set up network segmentation
- [ ] Configured firewalls
- [ ] Enabled audit logging
- [ ] Set up monitoring alerts
- [ ] Performed security scan
- [ ] Reviewed access controls
- [ ] Documented security procedures
- [ ] Trained team on security practices
- [ ] Set up backup and recovery
- [ ] Configured session timeouts
- [ ] Disabled unnecessary services
- [ ] Updated all dependencies
- [ ] Reviewed and minimized permissions

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Airflow Security Documentation](https://airflow.apache.org/docs/apache-airflow/stable/security/)
- [Grafana Security](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

---

## 🔄 Regular Security Maintenance

### Monthly
- [ ] Review access logs
- [ ] Update dependencies
- [ ] Scan for vulnerabilities
- [ ] Review user permissions

### Quarterly
- [ ] Rotate credentials
- [ ] Security audit
- [ ] Penetration testing
- [ ] Update security policies

### Annually
- [ ] Comprehensive security review
- [ ] Update disaster recovery plan
- [ ] Security training
- [ ] Compliance audit

---

**Remember: Security is not a one-time setup, it's an ongoing process!**
