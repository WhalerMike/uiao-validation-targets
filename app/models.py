from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, Field


class OSCALEvidence(BaseModel):
    """OSCAL-compatible evidence artifact for FedRAMP Rev 5 controls."""

    uuid: UUID
    title: str
    description: str
    collected_on: datetime
    control_id: str
    prop_id: str = Field(
        ...,
        description="Must match UIAO-MEMORY.md rule – must start with 'prop:'",
    )
    evidence_type: str = "artifact"


class TelemetryLog(BaseModel):
    """Telemetry event log entry emitted by a monitored system."""

    timestamp: datetime
    control_id: str
    event_type: str
    status: str
    details: Dict[str, Any]


class ValidationResponse(BaseModel):
    """Standard response returned after validating an inbound payload."""

    status: str
    message: str
    validated_against: str = "FedRAMP Rev 5 + OSCAL 1.3.0"
