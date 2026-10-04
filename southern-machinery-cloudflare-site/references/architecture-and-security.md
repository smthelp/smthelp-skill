# Architecture and Security

## Cloudflare Service Boundaries

- D1: products, inquiries, admins/users, roles, and other relational records.
- R2: uploaded product images and media.
- KV: site settings, lightweight configuration, or cacheable values; not authoritative auth state.
- Worker or Pages Function: routing, validation, authentication, authorization, storage access, and HTML/API responses.

## Authentication

- Hash passwords with PBKDF2-SHA256 and a cryptographically random unique salt per user.
- For Cloudflare WebCrypto compatibility, use no more than 100,000 PBKDF2 iterations unless the deployed runtime has been explicitly verified with a higher value. The known portable value is 100,000.
- Store algorithm, iteration count, salt, and derived hash so future upgrades are possible.
- Use constant-time comparison where the runtime permits it.
- Use a standards-compliant HS256 JWT implementation: base64url header and payload, HMAC-SHA256 signature, expiration, issued-at, and a stable subject. Validate algorithm and expiration on every protected request.
- Store the JWT signing secret as a Cloudflare Secret. Never put it in Wrangler variables, source, schema, fixtures, or Git.
- Prefer secure, HttpOnly, SameSite cookies for browser admin sessions when compatible with the app. If bearer tokens are used, minimize browser persistence and document the threat model.

## Authorization

Authentication is not authorization. Enforce roles on the server for every protected endpoint. Define a small permission matrix, for example:

| Capability | Admin | Super Admin |
|---|---:|---:|
| View inquiries | Yes | Yes |
| Update inquiry status | Yes | Yes |
| Upload product media | If granted | Yes |
| Manage admin accounts/roles | No | Yes |

Do not rely on hidden buttons or client-side route guards.

## API and Data Protection

- Define a shared browser API client in a common layout/module when multiple pages use it. Load it before page-specific scripts and test the rendered output, not only the source import graph.
- Centralize same-origin base URL, JSON parsing, HTTP status handling, and controlled error messages. Do not treat a parsed JSON error body as a successful request.
- Default to same-origin requests. Do not return wildcard CORS headers for credentialed or administrative APIs.
- Validate content type, body size, field length, enum values, email format, and required fields server-side.
- Use parameterized D1 queries.
- Avoid returning password fields, hashes, salts, internal errors, stack traces, or unnecessary personal data.
- Rate-limit login, RFQ, upload, and webhook-trigger endpoints when the platform plan permits it.
- Protect inquiry listing, status updates, admin management, upload, and webhook proxy endpoints.

## Authentication Incident Tests

When diagnosing login, distinguish client failure from authentication failure:

1. Confirm the login page loads and the browser has no missing-global or syntax errors.
2. Confirm the submit handler sends `POST /api/admin/login` only after the shared API client exists.
3. Verify an intentionally invalid password returns `401` with a generic message.
4. Verify an authorized test account returns `200`, a role, and a token/session without logging its value.
5. Use the returned session to call one protected endpoint and confirm the expected role boundary.
6. Delete temporary response/token files immediately after verification.

## Uploads and Webhooks

- Allowlist MIME types and extensions, cap file size, generate server-side object keys, and prevent path traversal.
- Treat browser-provided MIME type and filename as untrusted.
- Keep R2 write operations behind authorized server routes.
- Proxy authenticated n8n calls server-side. Store webhook URLs or credentials as secrets when sensitive.
- Apply timeouts and return controlled errors without leaking upstream responses.

## Seed Accounts

Never commit real default passwords or reusable hashes. Prefer a one-time bootstrap command that reads credentials from secure input, or create the first administrator through a protected setup flow that disables itself after use. Force rotation when temporary credentials are unavoidable.
