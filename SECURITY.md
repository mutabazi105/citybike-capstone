# Security Policy

## Supported Versions

| Version | Status | Support Until |
|---------|--------|----------------|
| 1.0.0   | Active | 2027-02-09 |
| < 1.0.0 | EOL    | Not Supported |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in CityBike Analytics Platform, please report it responsibly.

### Do NOT

❌ Do **NOT** open a public GitHub Issue for security vulnerabilities
❌ Do **NOT** publicly disclose the vulnerability before we've had time to patch
❌ Do **NOT** test the vulnerability on production systems

### DO

✅ Email: `mutabazi105@gmail.com` with subject line: `[SECURITY] CityBike Vulnerability Report`
✅ Include detailed description of the vulnerability
✅ Provide steps to reproduce (if applicable)
✅ Allow 48-72 hours for initial response
✅ Work with us to determine severity and fix timeline

### What to Include in Your Report

```
Title: Brief description of vulnerability

Description: 
- Detailed explanation of the issue
- Affected components/modules
- Potential impact

Reproduction Steps:
1. Step 1
2. Step 2
3. etc.

Severity Assessment:
- Critical / High / Medium / Low (your assessment)
- CVSS Score (if applicable)

Suggested Fix (optional):
- Any recommended solutions
```

## Security Considerations

### Current Security Posture

This is an **educational capstone project**, not a production system. Security considerations include:

#### ✅ What We Do

- Input validation on all user-provided data
- Type hints for type safety
- Proper error handling without information leakage
- Secure random data generation for synthetic data
- No hardcoded credentials or secrets
- HTTPS-ready code structure

#### ⚠️ Known Limitations

- No authentication/authorization system
- No encryption at rest
- No network security (assumes local/trusted environment)
- Sample data only (no real user data)
- No audit logging
- No rate limiting

### Production Deployment

If you plan to deploy CityBike to production, implement:

1. **Authentication & Authorization**
   - OAuth2 / JWT tokens
   - Role-based access control (RBAC)

2. **Data Security**
   - Encrypt sensitive data at rest (AES-256)
   - TLS/SSL for data in transit
   - Database encryption
   - Regular backups with encryption

3. **API Security**
   - Rate limiting
   - CORS configuration
   - Input validation & sanitization
   - SQL injection prevention
   - CSRF protection

4. **Monitoring & Logging**
   - Security event logging
   - Intrusion detection
   - Vulnerability scanning
   - Penetration testing

5. **Deployment Security**
   - Container image scanning (if using Docker)
   - Secrets management (HashiCorp Vault, AWS Secrets Manager)
   - Network segmentation
   - Web Application Firewall (WAF)

### Dependencies Security

We use well-maintained, industry-standard libraries:

- **pandas** - Widely used, actively maintained
- **numpy** - Core scientific Python library
- **matplotlib** - Standard visualization library
- **python-dateutil** - Trusted date/time utilities

**Recommendation:** Run `pip audit` regularly to check for known vulnerabilities:

```bash
pip install pip-audit
pip-audit
```

### Code Quality & Security

We follow these practices:

```bash
# Type checking
mypy citybike/ --strict

# Linting
pylint citybike/

# Code formatting
black citybike/

# Security checks
bandit -r citybike/

# Dependency auditing
pip-audit
```

## Security Best Practices

### For Users of This Project

1. **Review the code** - This is open source, examine what you're running
2. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`
3. **Use virtual environments** - Never install to system Python
4. **Monitor for updates** - Watch this repository for security notices
5. **Report issues responsibly** - Follow this security policy

### For Contributors

1. **Follow CONTRIBUTING.md guidelines**
2. **Use pre-commit hooks** - Run code quality checks before committing
3. **Add tests for security fixes** - Ensure fixes don't regress
4. **Document security changes** - Explain security improvements clearly
5. **Never commit secrets** - No API keys, passwords, or tokens

## Security Headers

If deploying as a web service, implement these HTTP headers:

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## Compliance & Standards

This project aims to follow:

- ✅ PEP 8 (Python style guide)
- ✅ Google Python Style Guide (docstrings)
- ✅ OWASP Top 10 (web application security)
- ✅ CWE/SANS Top 25 (software weaknesses)

## Changelog

Security updates will be documented in [CHANGELOG.md](CHANGELOG.md) with `[SECURITY]` tags.

## Questions?

For security-related questions (not vulnerabilities):
- 📧 Email: `mutabazi105@gmail.com`
- 🐙 Open a GitHub Discussion (for non-sensitive topics)

---

**Last Updated:** 2026-02-09

This security policy may be updated as the project evolves. Check back regularly for updates.
