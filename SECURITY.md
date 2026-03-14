# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 1.0.x | ✅ |
| < 1.0 | ❌ |

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Email: technical@cats-system.org  
Subject: `[SECURITY] <brief description>`

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

We aim to acknowledge receipt within **48 hours** and provide an initial assessment within **7 days**.

## Scope

- Authentication / authorisation bypass
- Injection vulnerabilities (SQL, command)
- Cryptographic weaknesses in audit log
- Rate-limit bypass
- Information disclosure in API responses

## Out of scope

- Theoretical vulnerabilities without PoC
- Issues in third-party dependencies (report to upstream)
- Issues requiring physical access
