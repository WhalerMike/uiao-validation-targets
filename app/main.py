from __future__ import annotations

from fastapi import FastAPI, HTTPException

from models import OSCALEvidence, TelemetryLog, ValidationResponse

app = FastAPI(
    title="uiao-validation-targets",
    description="Live mock application + telemetry endpoint for uiao-core "
    "(FedRAMP Moderate Rev 5 pre-implementation validation)",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# FedRAMP Moderate Rev 5 sample baseline – controls returned by the baseline
# endpoint and used for internal reference.
# ---------------------------------------------------------------------------
FEDRAMP_REV5_BASELINE = {
    "baseline": "FedRAMP Moderate Rev 5",
    "oscal_version": "1.3.0",
    "controls": [
        {
            "id": "AC-2",
            "title": "Account Management",
            "family": "AC",
            "impact": "Moderate",
            "description": (
                "Manage information system accounts, including establishing, "
                "activating, modifying, reviewing, disabling, and removing accounts."
            ),
            "fedramp_parameters": {
                "AC-2(a)": "Account types: individual, shared, group, system, guest/anonymous, emergency, developer, temporary, and service.",
                "AC-2(j)": "Reviews accounts every 365 days.",
            },
        },
        {
            "id": "IA-5",
            "title": "Authenticator Management",
            "family": "IA",
            "impact": "Moderate",
            "description": (
                "Manage information system authenticators for users and devices "
                "including initial distribution, replacement, and revocation."
            ),
            "fedramp_parameters": {
                "IA-5(1)(a)": "Minimum password complexity enforced.",
                "IA-5(1)(d)": "Passwords expire no longer than 60 days.",
            },
        },
        {
            "id": "CM-6",
            "title": "Configuration Settings",
            "family": "CM",
            "impact": "Moderate",
            "description": (
                "Establish and document configuration settings for information "
                "technology products employed within the information system."
            ),
            "fedramp_parameters": {
                "CM-6(a)": "USGCB/DISA STIGs used as configuration baselines.",
            },
        },
        {
            "id": "SI-4",
            "title": "Information System Monitoring",
            "family": "SI",
            "impact": "Moderate",
            "description": (
                "Monitor the information system to detect attacks and indicators "
                "of potential attacks in accordance with monitoring objectives."
            ),
            "fedramp_parameters": {
                "SI-4(a)": "Monitors inbound and outbound communications traffic.",
                "SI-4(b)": "Identifies unauthorized use of the information system.",
            },
        },
    ],
}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health", summary="Health check")
def health() -> dict:
    """Return service liveness and FedRAMP baseline metadata."""
    return {
        "status": "healthy",
        "target_name": "uiao-validation-targets",
        "fedramp_baseline": "FedRAMP Moderate Rev 5",
        "oscal_version": "1.3.0",
    }


@app.post(
    "/ingest-evidence",
    response_model=ValidationResponse,
    summary="Ingest OSCAL evidence artifact",
)
def ingest_evidence(evidence: OSCALEvidence) -> ValidationResponse:
    """
    Accept an OSCALEvidence payload, validate that *prop_id* starts with
    ``prop:``, and return a ValidationResponse.
    """
    if not evidence.prop_id.startswith("prop:"):
        raise HTTPException(
            status_code=422,
            detail=(
                f"prop_id '{evidence.prop_id}' is invalid – "
                "must start with 'prop:' per UIAO-MEMORY.md rule."
            ),
        )
    return ValidationResponse(
        status="valid",
        message=(
            f"Evidence '{evidence.title}' for control {evidence.control_id} "
            "accepted and validated."
        ),
    )


@app.post(
    "/telemetry",
    response_model=ValidationResponse,
    summary="Ingest telemetry log event",
)
def ingest_telemetry(log: TelemetryLog) -> ValidationResponse:
    """Accept a TelemetryLog event and return a ValidationResponse."""
    return ValidationResponse(
        status="received",
        message=(
            f"Telemetry event '{log.event_type}' for control {log.control_id} "
            f"received with status '{log.status}'."
        ),
    )


@app.get(
    "/validation/fedramp-rev5-baseline",
    summary="FedRAMP Moderate Rev 5 control baseline",
)
def fedramp_rev5_baseline() -> dict:
    """Return a sample FedRAMP Moderate Rev 5 control baseline (AC-2, IA-5, CM-6, SI-4)."""
    return FEDRAMP_REV5_BASELINE
