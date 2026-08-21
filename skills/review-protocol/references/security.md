---
name: security-review
description: Security-focused code review checklist covering secrets, input validation, injection, auth, IDOR, abuse protection, data exposure, dependencies, transport, and deployment. Load when the changed code touches user input, authentication, API endpoints, file operations, database queries, or sensitive data.
---

## Checklist

### Secrets and Credentials
- [ ] No hardcoded API keys, tokens, passwords, or connection strings
- [ ] Secrets loaded from environment variables or a vault, never from source
- [ ] `.env` files listed in `.gitignore`
- [ ] No secrets in logs, error messages, or stack traces
- [ ] Secrets never exposed in frontend bundles, public config, or client-readable env vars
- [ ] Database credentials, service keys, and admin tokens used only on trusted server-side components

### Input Validation
- [ ] All input entry points mapped and reviewed: forms, JSON bodies, query params, path params, headers, uploads, webhooks, external API payloads
- [ ] All external input validated server-side (not just client)
- [ ] Data types, lengths, ranges, and schemas enforced before use
- [ ] Allowlists preferred over denylists for accepted values
- [ ] Invalid input rejected early with consistent error handling
- [ ] Sanitization applied when user-controlled content can reach HTML/templates, shell commands, or file paths
- [ ] File uploads: type, size, extension, and filename validated; stored outside webroot

### Injection Prevention
- [ ] SQL: parameterized queries or ORM — never string concatenation or f-strings
- [ ] Command injection: no `os.system()` or `subprocess.run(shell=True)` with user input
- [ ] Path traversal: user input never used directly in file paths without sanitization
- [ ] Template injection: user input never passed raw into template engines
- [ ] Script injection (XSS): user-controlled content escaped or sanitized before rendering

### Authentication and Authorization
- [ ] Passwords hashed with bcrypt or argon2 (not MD5, SHA1, or plain text)
- [ ] Session tokens are random, long, and rotated on auth state changes
- [ ] Email verification enforced where applicable before granting full account access
- [ ] Password reset tokens are random, short-lived, and single-use
- [ ] Session cookies use secure flags (`HttpOnly`, `Secure`, appropriate `SameSite`)
- [ ] Authorization checked on every request, not just at login
- [ ] API keys and tokens transmitted via headers, never in URLs
- [ ] Failed auth returns generic error messages (no "user not found" vs "wrong password")
- [ ] Login and auth endpoints are rate-limited
- [ ] Auth/session secrets never exposed to frontend code, browser storage, or client-side env vars

### Object Authorization (IDOR)
- [ ] Resource reads verify requester ownership or explicit permission
- [ ] Updates, deletes, and state-changing actions enforce object-level authorization
- [ ] Route/query IDs never trusted without ownership checks
- [ ] Multi-tenant boundaries enforced in query filters and service-layer access
- [ ] APIs do not allow predictable object access without authorization guards

### Abuse Protection
- [ ] Login, signup, and password reset endpoints are rate-limited
- [ ] Public API endpoints are rate-limited based on abuse risk and request cost
- [ ] High-cost endpoints (AI generation/export/search) have stricter controls
- [ ] Repeated automated requests can be detected and throttled or blocked
- [ ] Abuse controls do not rely only on frontend restrictions

### Data Exposure
- [ ] API responses contain only the fields the client needs
- [ ] Error responses do not leak stack traces, SQL queries, or internal paths
- [ ] Logs do not contain PII, passwords, or tokens
- [ ] Debug mode disabled in production configs

### Dependencies

**Environment detection:**
- Python project (`pyproject.toml` or `requirements.txt`): run `pip-audit` or `uv run pip-audit`
- Node project (`package.json`): run `pnpm audit` or `npm audit`

**Checklist:**
- [ ] No known-vulnerable dependencies (`pip-audit` or `pnpm audit`)
- [ ] Dependencies pinned to specific versions (no `*` or loose ranges in production code)
- [ ] Minimal dependency surface — each one is justified
- [ ] Lockfile committed (`uv.lock`, `pnpm-lock.yaml`, or `package-lock.json`)

**Node/JS supply chain hardening:**
- [ ] `ignore-scripts=true` in `.npmrc` or global config
- [ ] pnpm preferred over npm — built-in protections (1-day Minimum Release Age, exotic subdependency blocking)
- [ ] Version pinning: exact versions, not ranges, for production
- [ ] Audit transitive dependencies: `pnpm list --depth=10` or `npm ls`

### Transport and Storage
- [ ] Sensitive data encrypted at rest
- [ ] All external communication over HTTPS/TLS
- [ ] CORS configured restrictively (not `*` in production)

### Deployment and Monitoring
- [ ] Production databases and internal services not publicly reachable unless explicitly required
- [ ] Debug/admin endpoints disabled or strongly protected in production
- [ ] Failed authentication and suspicious access patterns logged safely for detection
- [ ] API errors logged with enough operational signal without leaking secrets
- [ ] Monitoring or alerts exist for unusual traffic, auth abuse, or repeated failure patterns

### CI/CD Pipeline Security
- [ ] GitHub Actions workflows pin third-party actions to a specific SHA commit (not `@main` or `@v1` tag)
- [ ] No script injection vectors: `run:` steps avoid `${{ github.event.* }}` interpolation without sanitization
- [ ] `GITHUB_TOKEN` permissions set to minimal scope
- [ ] Workflow files do not contain hardcoded secrets, tokens, or credentials
- [ ] Third-party actions vetted: check source repo, usage count, recent commits before adopting; pin to SHA
- [ ] Self-hosted runners (if used) isolated from the internet and cleaned between runs
- [ ] CI/CD secrets scoped per-environment

### Container and Docker Security
- [ ] Dockerfile declares a `USER` other than root unless explicitly justified
- [ ] `FROM` tag pinned to a specific version digest (not `:latest` or mutable tag)
- [ ] Secrets never passed as build args or `ENV` — use BuildKit `--secret` or runtime injection
- [ ] Multi-stage builds used to keep final image small
- [ ] `.dockerignore` exists and excludes `node_modules`, `.git`, secrets, build caches
- [ ] `HEALTHCHECK` defined for production containers
- [ ] Docker Compose: no `privileged: true`, `network_mode: host`, or unrestricted `0.0.0.0` unless justified

### Infrastructure as Code Security (if project uses Terraform, Pulumi, or CloudFormation)
- [ ] S3 buckets (or equivalent) enforce server-side encryption and block public access by default
- [ ] Security group/firewall rules do not allow unrestricted ingress (0.0.0.0/0) to sensitive ports (22, 3389, database ports)
- [ ] IAM roles and policies avoid wildcard (`*`) actions unless scoped to a specific service
- [ ] Storage and databases do not have `publicly_accessible = true` unless required and documented
- [ ] Encryption in transit and at rest enforced
- [ ] Mandatory resource tags enforced via policy
- [ ] Terraform remote state stored in encrypted backends (S3 + DynamoDB lock, GCS, Terraform Cloud)
- [ ] Infrastructure changes go through plan review and automated scanning before apply

### Python-Specific Vulnerabilities

#### Critical — Arbitrary Code Execution
- [ ] No `eval()` or `exec()` on untrusted input
- [ ] No `pickle.loads()` on untrusted data — use `json` or `msgpack`
- [ ] No `yaml.load()` without SafeLoader — use `yaml.safe_load()`
- [ ] No `subprocess.run(shell=True)` with user input

#### High — Command Injection
- [ ] No `os.system()` or `os.popen()` with user input
- [ ] Shell commands use `shlex.quote()` if shell is unavoidable
- [ ] `subprocess` calls use list args, not string concatenation

#### Medium — Weak Cryptography
- [ ] `secrets` module for tokens, not `random`
- [ ] `bcrypt` or `argon2` for password hashing, not `md5`/`sha1`

#### Low — DoS and Info Disclosure
- [ ] `requests` calls have explicit timeout
- [ ] No `tarfile.extract()` without filter (path traversal risk)
- [ ] No `str.format()` on untrusted templates (format string attack)

## Severity Ratings

- **Critical** — exploitable now: secrets in code, SQL injection, auth bypass
- **High** — likely exploitable: missing input validation, weak crypto, path traversal
- **Medium** — conditional risk: verbose errors, overly permissive CORS, missing rate limits
- **Low** — hardening: dependency updates, logging improvements, header security

Report only findings that apply to the actual code under review. Do not flag checklist items not relevant to the codebase.
