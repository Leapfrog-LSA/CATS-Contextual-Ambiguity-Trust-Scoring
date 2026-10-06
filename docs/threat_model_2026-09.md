# Threat model — technical draft (September 2026)

> **Draft for human review.** This is the technical part of the risk
> register's R8 item ("Pen-test / threat model — TODO",
> [`eu_ai_act/risk_management_art9.md`](eu_ai_act/risk_management_art9.md)).
> It was written from a read of the code at `main` on 27 Sep 2026, not from a
> penetration test. The ratings are a proposed technical triage (likelihood ×
> impact for the bundled `docker-compose.yml` deployment). They are for the
> maintainer to accept or change. Nothing here is a legal or compliance
> determination, and the R8 row itself is left untouched for its owner. The
> penetration test still needs an external reviewer.

## Scope

| In scope | Out of scope |
|---|---|
| The FastAPI deployment as shipped: `deploy/nginx.conf` → `app` (uvicorn) → Postgres 16 + Redis 7 (`docker-compose.yml`, `Dockerfile`) | The host OS, cloud account and network of a particular deployment |
| The library surfaces that fetch external content: `cats.lite.score_feed`, the MCP server (`cats/mcp_server.py`), the RSS collector (`cats/calibration/collect_rss.py`) | Model-level manipulation of the score by adversarial *sources*. That is a model risk, tracked in the risk register and exercised by `tests/unit/test_adversarial.py` |
| Build and release: CI, the Docker image, PyPI trusted publishing | Legal classification, data-protection determinations, sign-offs (human TODOs in `eu_ai_act/`) |

## System and trust boundaries

```
Internet ──► nginx :80 ──► app :8000 (expose only) ──► Postgres :5432
  (untrusted)  │ rate limit, 2 MB cap,     │ API-key auth,      └─► Redis :6379
               │ XFF overwrite, /metrics   │ tenant scoping,
               │ denied                    │ AES-GCM audit
               ▼
         (TLS: HTTPS block commented out — see T11)

LLM client ──► MCP server ──► arbitrary feed URLs (outbound HTTP)
Scheduled job ──► collect_rss ──► registry feed URLs (outbound HTTP)
```

The boundaries that matter:
1. **Internet → nginx.** Every request is untrusted.
2. **nginx → app.** The app trusts nginx's `X-Forwarded-For` (T3).
3. **app → Postgres/Redis.** Trusted network, but see T2.
4. **CATS → external feeds.** Untrusted content and untrusted URLs (T9).
5. **Maintainer → PyPI.** Supply chain (T10).

## Assets

| Asset | Where | Why it matters |
|---|---|---|
| API keys (`CATS_API_KEY`, `_PREV`, `CATS_API_KEYS`) | env / `.env` | Full access to a tenant's scoring, explanations, contests |
| Tenant data | `trust_scores` (score, signals, client `context`), `contests` (free-text reasons and responses) | Confidentiality between tenants; the free text may contain personal data |
| Audit trail | `audit_logs` (AES-GCM payload, plaintext `ip_address`) | Accountability for automated decisions (GDPR Art. 22 contest flow) |
| `AUDIT_ENCRYPTION_KEY` | env | Decrypts every audit payload |
| Service availability | the single NLP thread per process (`_NLP_EXECUTOR`) | One slow request delays every tenant (T1) |
| Score integrity | `data/calibrated_weights.json`, signal code | A tampered table or package silently changes every score |
| The published package | PyPI `cats-scoring` | Users install it directly |

## Controls already in place (verified in code)

| Control | Where |
|---|---|
| Constant-time API-key comparison (`hmac.compare_digest`) | `cats/core/security.py` `verify_api_key`, `resolve_tenant` |
| Tenant bound server-side to the key, never client-supplied | `resolve_tenant` |
| Every read filtered by `tenant_id` (`/explain`, `/contest`, `/contest/{id}/resolve`, `/review`, `/stats`) | `cats/api/routes/evaluate.py` |
| Failed authentications rate-limited per client IP; valid keys per hashed key (Redis sliding window) | `APIKeyBearer`, `rate_limit_id` |
| nginx: 30 req/min/IP (burst 10), 2 MB body cap, `X-Forwarded-For` overwritten (not appended), `nosniff` / `DENY` / `no-referrer` headers | `deploy/nginx.conf` |
| `/metrics` not served by the public proxy | `deploy/nginx.conf` (#163) |
| Schema limits on every input (500 messages, 10 000 chars, 50 batch items, ISO timestamps) | `cats/api/schemas.py` |
| SQL via the SQLAlchemy ORM (parameterised) | routes, `cats/audit/logger.py` |
| Generic `500` body (RFC 7807), cause only logged server-side | `cats/api/main.py` |
| Audit payload encrypted with AES-256-GCM, random 96-bit nonce | `cats/audit/logger.py` |
| Container runs as non-root `cats`; app port `expose`d only, not published | `Dockerfile`, `docker-compose.yml` |
| PyPI publishing via OIDC trusted publishing (no long-lived token) | `.github/workflows/release.yml` |
| Collector: response size cap, timeouts; `curl` fallback run without a shell (argument list) | `cats/calibration/collect_rss.py` |

## Threats and gaps

Proposed rating: **H**igh / **M**edium / **L**ow / **Info**, for the bundled
deployment.

| ID | STRIDE | Threat | Rating | Recommendation |
|---|---|---|---|---|
| T1 | DoS | NLP queue monopolised by one valid key | M | Cap total text per request, per-tenant concurrency limit |
| T2 | I, T, E | Postgres and Redis published on the host with default credentials | M | Remove `ports`, set passwords, Redis `requirepass` |
| T3 | S, R | `X-Forwarded-For` trusted by default | M | Default `trust_proxy_headers` to off |
| T4 | R, E | No separation between scoring clients and contest reviewers | M | Reviewer role and identity |
| T5 | I | Retention covers only the audit log; IP kept in plaintext | M | Retention policy for all tables |
| T6 | T | Audit ciphertext not bound to its row; no key rotation | L | AAD and a key id |
| T7 | S | No API-key strength check; manual rotation | L | Startup length check |
| T8 | I | OpenAPI docs and `/health` public by default | L | Disable docs in production |
| T9 | S, I, D | SSRF and memory exhaustion in feed fetching (library, MCP) | L–M | Block private ranges, stream with a cap |
| T10 | T | No dependency or code scanning in CI | L | Dependabot, `pip-audit` |
| T11 | — | Security docs that do not match the code | Info | Correct by their owners |

### T1 — NLP queue monopolised by one valid key (DoS) — **M**

Since #166 each process runs coherence on **one** NLP thread shared by every
request. A request costs about 25–40 µs per character of text
([`load_test_2026-09.md`](load_test_2026-09.md)). The 2 MB body cap admits
about 2 M characters, so one request can take 50–80 s of that thread. A single
key can send 30 such requests a minute, the per-key limit. So one tenant, or a
leaked key, can hold the NLP thread for all tenants indefinitely.

Through nginx the client gets a `504` at 30 s. Whether the app then abandons
or finishes the work was not checked.

**Recommend:**
- cap the total text per request well below what the proxy timeout allows;
- a per-tenant concurrency limit on the NLP queue;
- optionally, cancel work whose client has disconnected.

### T2 — Postgres and Redis published on the host with default credentials — **M**

`docker-compose.yml` publishes `5432:5432` and `6379:6379`. Postgres uses
`cats`/`cats`, and Redis has no password. On a host without a firewall, both
are reachable from outside, bypassing nginx and the app entirely:
- read or alter every tenant's data;
- flush the rate-limit state.

This contrasts with the app itself, which the same file deliberately only
`expose`s.

**Recommend:**
- drop the `ports:` entries, or bind them to `127.0.0.1` for local
  development;
- take the Postgres password from `.env`;
- set Redis `requirepass`.

> **Status (30 Sep 2026): addressed in `docker-compose.yml`.**
> - Both ports are bound to `127.0.0.1`, so local development and tests still
>   reach them from the host, and nothing outside does.
> - `POSTGRES_PASSWORD` comes from `.env`. The development fallback `cats` is
>   used only when it is unset.
> - With `REDIS_PASSWORD` set, Redis starts with `--requirepass`, and the
>   healthcheck authenticates with the same password.

### T3 — `X-Forwarded-For` trusted by default — **M**

`trust_proxy_headers` defaults to `True`. Behind the bundled nginx this is safe,
because nginx overwrites the header. If the app is reached directly (another
proxy that appends, or the port published by mistake), a client can set any
IP. That lets it:
- forge the IP recorded in the audit log (repudiation);
- rotate addresses to escape the failed-authentication limiter.

**Recommend:** default `trust_proxy_headers` to `False`, and enable it
explicitly in the compose environment next to the nginx that justifies it.

> **Status (30 Sep 2026): addressed.** The code default is now `False`.
> `docker-compose.yml` sets `TRUST_PROXY_HEADERS: "true"` on the app service,
> next to the nginx that overwrites the header.

### T4 — No separation between scoring clients and contest reviewers — **M**

Any valid key of a tenant can call `/contest/{id}/resolve`, the human decision
on a GDPR Art. 22 appeal. The same automated client that submits evaluations
can therefore also close appeals. The resolution records no reviewer identity. `contests` has no
column for who resolved an appeal (its `user_id` refers to whoever filed it,
and is never set), and the audit entry for the resolution carries only the
client IP.

This is a technical accountability gap. Whether it meets Art. 22 is a legal
question for a human.

**Recommend:** a separate reviewer credential or role for resolve (and review),
and store who resolved.

### T5 — Retention covers only the audit log; IP kept in plaintext — **M**

`purge_expired_audits` deletes `audit_logs` older than `AUDIT_RETENTION_DAYS`
(90). It never deletes `trust_scores`, which holds the client-supplied
`context`, or `contests`, which holds free-text reasons that may contain
personal data. `audit_logs.ip_address` is stored in plaintext next to the
encrypted payload.

**Recommend:**
- a retention decision for every table (human);
- apply it in the purge job;
- consider truncating or hashing stored IPs.

### T6 — Audit ciphertext not bound to its row; no key rotation — **L**

AES-GCM is called with no associated data. A ciphertext therefore still
decrypts if someone with database write access moves it to another row or
tenant. There is also a single `AUDIT_ENCRYPTION_KEY` with no key id, so it
cannot be rotated without re-encrypting everything.

**Recommend:**
- use `tenant_id` + `trace_id` as associated data for new rows (needs a
  compatibility path for existing ones);
- prefix blobs with a key id.

### T7 — API-key strength and lifecycle — **L**

Nothing checks a key's length or entropy at start-up. A short key makes the
per-IP failed-auth limiter the only barrier. Keys are long-lived environment
secrets with one rotation slot (`CATS_API_KEY_PREV`).

**Recommend:**
- refuse to start with keys under, say, 32 characters;
- document the rotation procedure.

> **Status (6 Oct 2026): addressed.** At startup, `check_api_key_strength`
> (`cats/core/security.py`) checks `CATS_API_KEY`, `CATS_API_KEY_PREV` and every
> `CATS_API_KEYS` entry against a 32-character minimum.
> - With `ENVIRONMENT=production` (the default) a short key stops the API from
>   starting. The error names the variable or tenant, never the key.
> - Other environments log `api_key_weak` and start, so development and the
>   test suites keep short keys.
>
> The rotation procedure is in `docs/api.md`. Not done: an entropy check (a long
> but guessable key passes) and automatic rotation.

### T8 — OpenAPI docs and health details are public by default — **L**

FastAPI serves `/docs`, `/redoc` and `/openapi.json` by default, and nginx
proxies them. `/health` is unauthenticated and returns component status and
the version.

**Recommend:** disable the docs outside development (`docs_url=None`,
`openapi_url=None`), or restrict them in nginx. Keep `/health` minimal or
internal.

> **Status (1 Oct 2026): docs addressed; `/health` kept as is.**
> - **Docs:** `/docs`, `/redoc` and `/openapi.json` are now opt-in
>   (`CATS_API_DOCS`, off by default), and the app returns `404` for them
>   otherwise.
> - **`/health`:** it keeps its version field on purpose. `CLAUDE.md` makes
>   "the API reports `cats.__version__`" part of the release contract, and
>   load balancers and monitors need the endpoint from outside. It still
>   returns no error details: they are logged, not sent. Restrict it in nginx
>   if the version should not be public.

### T9 — SSRF and memory exhaustion in feed fetching (library, MCP) — **L–M**

`score_feed` and the MCP tool `score_source` fetch any URL the caller gives
them and follow redirects. So does the collector's `curl` fallback. There is no
block on private, loopback or link-local addresses, such as a cloud metadata
endpoint.

Through the MCP server, the URL comes from an LLM, which prompt injection can
steer. Content comes back only if it parses as RSS/Atom, which limits
exfiltration but does not stop internal requests.

`fetch_feed` also reads the whole response before checking `max_bytes`, so a
huge or endless response is held in memory.

**Recommend:**
- resolve the host and refuse private ranges, re-checking after every redirect;
- stream the body and stop at the cap.

> **Status (2 Oct 2026): addressed.** New `cats/core/url_guard.py`:
> `check_url` allows only http(s) and resolves the host, refusing the URL
> unless every address is globally routable (loopback, private, link-local and
> metadata, CGNAT, IPv4-mapped forms included). `fetch_feed` now follows
> redirects itself and checks every hop before requesting it. The `curl`
> fallback no longer uses `-L`: it follows redirects one checked hop at a
> time. The body is streamed and the read stops past `max_bytes`.
> `score_feed` and the MCP `score_source` refuse an unsafe URL with
> `UnsafeURLError` (CLI exit 3); an unsafe `<link>` found on a page is
> skipped. `allow_private=True` (library only) lifts the address check for
> deliberate local use.
> - **Residual risk:** DNS rebinding. The host is resolved by the check and
>   again by the HTTP client, so a host that answers differently between the
>   two lookups is not stopped. Closing it needs connection-level IP pinning.
> - **Also not covered:** a host that does not resolve locally (e.g. behind a
>   proxy that resolves names itself) passes the check and fails or succeeds
>   at fetch time as before.

### T10 — Supply chain — **L**

CI runs no dependency scanning (no Dependabot, no `pip-audit`) and no code
scanning. Requirements are ranges without hashes. The base image is pinned by
tag (`python:3.11-slim`), not by digest. Publishing already uses OIDC trusted
publishing.

**Recommend:** Dependabot for `pip`, GitHub Actions and Docker, plus a
`pip-audit` job in CI.

> **Status (1 Oct 2026): dependency scanning added; hashes and digest not.**
> - **`pip-audit`** (`.github/workflows/audit.yml`) runs on every PR, on push
>   to `main` and weekly. It fails on any known vulnerability in
>   `requirements.txt`, which is what the image installs. The development
>   tools are reported but do not fail the job.
> - **First run** found four affected packages:
>   - `cryptography` 49.0.0 (GHSA-g6cj-pr64-35w5, PKCS#7 decryption).
>     CATS only uses AES-GCM, so it was not exposed. The floor is raised to
>     50.0 anyway.
>   - `nltk` 3.10.3, via TextBlob (GHSA-8mgp-746c-j5xp, path handling in
>     model save/load). No fixed release exists yet. CATS never passes a
>     path to NLTK, so the advisory is ignored in the workflow, with the
>     reason written there. Remove the ignore once a fix ships.
>   - `black` 24.10 and `pytest` 8.4 are dev tools only. Their fixes are
>     major upgrades (black 26, pytest 9), left to Dependabot PRs.
> - **Dependabot** (`.github/dependabot.yml`) proposes weekly updates for
>   `pip` and GitHub Actions, and monthly updates for the Docker base image.
> - **Not done:** hash-pinned requirements, a digest-pinned base image and
>   code scanning (CodeQL). Dependabot alerts and security updates are
>   repository settings that a maintainer must enable.

### T11 — Security documentation that does not match the code — **Info**

These are left for their owners:
- **JWT:** the risk register's R8 row lists "API-key+JWT auth", and
  `annex_iv_technical_documentation.md` mentions "RS256 JWT support". The code
  has no JWT; authentication is API keys only.
- **TLS 1.3:** claimed, but the HTTPS server block is commented out. This is a
  known Fase 1 decision.
- **`SECURITY.md`:** it lists 1.6.x as the supported version while the current
  release is 1.7.0. Its contact address is still unverified.

## Suggested order

1. **Deployment defaults:** T2 and T3 are configuration-only.
2. **Availability:** T1 is a per-request text cap and a tenant concurrency
   limit.
3. **T4 and T5.** Both need a human decision (reviewer model, retention
   periods) before any code.
4. **T8 and T10.** Small and mechanical.
5. **T6, T7 and T9.** Hardening.

Then the external penetration test, against the result.
