# Security Policy

## Supported versions

Only the latest released version receives security fixes.

| Version | Supported |
|---|---|
| 1.11.x | ✅ |
| < 1.11 | ❌ |

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report it privately through GitHub: open the repository's **Security** tab and
choose **Report a vulnerability**
([private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)).
Only the maintainers can see the report.

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
