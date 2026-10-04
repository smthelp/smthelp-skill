# Clawto GPT Image 2 Gateway Notes

Observed in-session behavior for https://api.clawto.link:

- GET /v1/models with a valid Bearer token returns 200 and includes:
  - gpt-image-2
  - gpt-5.2
  - gpt-5.3-codex
  - gpt-5.3-codex-spark
  - gpt-5.4
  - gpt-5.4-mini
  - gpt-5.5
- GET /v1/models without credentials returns 401 Unauthorized.
- GET /v1/images/generations returned 404 Not Found in this session.
- GET /v1/chat/completions returned 404 Not Found in this session.
- POST /v1/responses returned 426 Upgrade Required in this session.
- The gateway therefore appears OpenAI-compatible for model listing, but its image generation path is not the standard /v1/images/generations endpoint.

Operational consequence:

- Always verify /v1/models and image generation on the same base URL and with the same credentials.
- Do not assume the existence of gpt-image-2 in /v1/models guarantees that the standard OpenAI image endpoint will work.
