# uiao-validation-targets

Live mock application + telemetry endpoint for **uiao-core** (FedRAMP Moderate Rev 5 pre-implementation validation).

---

## Overview

This repository provides a Docker-ready FastAPI service that uiao-core uses to:

1. **Ingest OSCAL evidence artifacts** – validates `prop:id` format required by
   `UIAO-MEMORY.md` and returns a `ValidationResponse`.
2. **Receive telemetry events** – accepts structured log events keyed to
   FedRAMP Moderate Rev 5 control IDs.
3. **Serve a FedRAMP Rev 5 control baseline** – returns AC-2, IA-5, CM-6, and
   SI-4 control metadata in JSON format.

All evidence payloads are validated against **OSCAL 1.3.0** and the
**FedRAMP Moderate Rev 5** baseline.

---

## Repository Structure

```
uiao-validation-targets/
├── app/
│   ├── main.py               # FastAPI application
│   ├── models.py             # Pydantic v2 OSCAL-compatible models
│   └── requirements.txt      # Pinned Python dependencies
├── telemetry/
│   ├── logs/
│   │   └── sample-audit-log.json         # 10 sample audit events
│   ├── metrics/
│   │   └── prometheus-sample.txt         # Prometheus exposition format
│   └── oscal-evidence/
│       ├── ac-2-evidence.json            # OSCAL 1.3.0 AC-2 evidence
│       └── ia-5-evidence.json            # OSCAL 1.3.0 IA-5 evidence
├── validation/
│   ├── fedramp-rev5-baseline.json        # FedRAMP Moderate Rev 5 baseline
│   └── oscal-1.3.0-schema/
│       └── README.md                     # Schema download instructions
├── .github/
│   └── workflows/
│       └── validate-endpoint.yml         # CI workflow
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose v2
- `curl` and `jq` (for manual testing)

### Start the service

```bash
docker compose up --build
```

The API is available at **http://localhost:8000**.

Interactive docs: **http://localhost:8000/docs**

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/health` | Service liveness + FedRAMP baseline metadata |
| `POST` | `/ingest-evidence` | Accept an OSCAL evidence artifact; validates `prop:id` |
| `POST` | `/telemetry` | Accept a structured telemetry event |
| `GET`  | `/validation/fedramp-rev5-baseline` | FedRAMP Moderate Rev 5 control baseline |

---

## curl Examples

### Health check

```bash
curl -s http://localhost:8000/health | jq .
```

Expected response:

```json
{
  "status": "healthy",
  "target_name": "uiao-validation-targets",
  "fedramp_baseline": "FedRAMP Moderate Rev 5",
  "oscal_version": "1.3.0"
}
```

---

### Ingest OSCAL evidence

```bash
curl -s -X POST http://localhost:8000/ingest-evidence \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "a3f1e2c4-d5b6-4789-a0b1-c2d3e4f56789",
    "title": "AC-2 Account Management Evidence",
    "description": "Quarterly account review completed with no anomalies.",
    "collected_on": "2026-03-24T00:00:00Z",
    "control_id": "AC-2",
    "prop_id": "prop:ac-2-evidence-001"
  }' | jq .
```

Expected response:

```json
{
  "status": "valid",
  "message": "Evidence 'AC-2 Account Management Evidence' for control AC-2 accepted and validated.",
  "validated_against": "FedRAMP Rev 5 + OSCAL 1.3.0"
}
```

> **Note:** `prop_id` **must** start with `prop:` – otherwise the endpoint
> returns HTTP 422 with a descriptive error.

---

### Submit telemetry event

```bash
curl -s -X POST http://localhost:8000/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2026-03-24T00:00:01Z",
    "control_id": "IA-5",
    "event_type": "password_changed",
    "status": "success",
    "details": {
      "username": "alice.smith",
      "complexity_check": "passed",
      "days_until_expiry": 60
    }
  }' | jq .
```

---

### FedRAMP Rev 5 baseline

```bash
curl -s http://localhost:8000/validation/fedramp-rev5-baseline | jq .controls
```

---

## How uiao-core Consumes This Endpoint

uiao-core:

1. Sends `POST /ingest-evidence` with OSCAL evidence payloads keyed to
   FedRAMP Rev 5 control IDs. The `prop_id` field **must** match the
   `prop:<id>` format defined in `UIAO-MEMORY.md`.
2. Polls `GET /health` to confirm the target is reachable before running
   validation sweeps.
3. Queries `GET /validation/fedramp-rev5-baseline` to retrieve the authoritative
   control list for a validation run.
4. Posts telemetry events to `POST /telemetry` for every monitored control
   action.

All evidence UUIDs are **UUIDv4** format. All evidence files include a
`prop:id` property consistent with OSCAL 1.3.0 naming conventions.

---

## CI / Validation Workflow

The `.github/workflows/validate-endpoint.yml` workflow:

- Builds the Docker image and starts the service.
- Runs smoke tests against all endpoints including a negative test for invalid
  `prop_id`.
- Validates that static OSCAL evidence files contain a `prop:id` property and
  a valid UUIDv4.
- Runs **pip-audit** to check for known CVEs in Python dependencies.
- Supports manual triggering via `workflow_dispatch`.

---

## FedRAMP POA&M Enum Values

The following values are valid for the `prop:poa-m-status` field in OSCAL
evidence documents:

- `open`
- `closed`
- `risk-accepted`
- `false-positive`
- `operational-requirement`
- `vendor-dependency`
- `not-applicable`

---

## Dependencies

| Package | Version |
|---------|---------|
| fastapi | 0.115.0 |
| uvicorn[standard] | 0.32.0 |
| pydantic | 2.10.0 |
| python-multipart | 0.0.22 |

---

## License

See repository root for license information.
