# Security Policy

## Supported Versions

SM Analytics is currently under active development.

Security updates are provided only for the latest development branch until the first stable release.

| Version | Supported |
|----------|-----------|
| Main (development) | ✅ |
| Released versions | Not yet available |

---

# Reporting a Vulnerability

If you discover a security vulnerability, **please do not open a public GitHub Issue**.

Instead, report it privately by contacting the project maintainer.

Please include:

- Description of the vulnerability
- Steps to reproduce
- Affected component(s)
- Potential impact
- Proof of Concept (if available)
- Suggested mitigation (optional)

A report should contain enough information for the issue to be reproduced and validated.

---

# Response Process

Security reports will generally follow this process:

1. Acknowledge receipt of the report.
2. Validate the vulnerability.
3. Assess severity and impact.
4. Develop and test a fix.
5. Release the fix.
6. Publicly disclose the vulnerability after remediation, when appropriate.

---

# Scope

Examples of issues that may be considered security vulnerabilities include:

- Authentication bypass
- Authorization flaws
- Privilege escalation
- SQL Injection
- Command Injection
- Remote Code Execution (RCE)
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Server-Side Request Forgery (SSRF)
- Sensitive data exposure
- Insecure deserialization
- Dependency vulnerabilities
- Denial of Service (DoS) vulnerabilities caused by implementation defects
- Security misconfigurations
- Secrets or credential exposure

---

# Out of Scope

The following generally do not qualify as security vulnerabilities:

- Requests for new security features
- Missing best practices without an exploitable impact
- Denial of Service caused solely by unrealistic resource exhaustion
- Issues in unsupported or modified environments
- Vulnerabilities in third-party software that have not been introduced by this project

---

# Security Best Practices

Contributors are expected to:

- Never commit secrets, API keys, or credentials.
- Validate and sanitize all external input.
- Apply the principle of least privilege.
- Keep dependencies up to date.
- Follow secure coding practices.
- Write security-focused tests where appropriate.

---

# Responsible Disclosure

Please allow reasonable time for a fix before publicly disclosing a vulnerability.

Coordinated disclosure helps protect users while a remediation is prepared and released.

---

# Security Updates

Security advisories and remediation guidance will be published with future releases as the project matures.
