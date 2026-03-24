# OSCAL 1.3.0 JSON Schemas

This directory is a placeholder for OSCAL 1.3.0 JSON schemas used to validate
OSCAL evidence documents in this repository.

## Where to Get the Schemas

Download the official OSCAL 1.3.0 JSON schemas from the NIST OSCAL GitHub
repository:

```
https://github.com/usnistgov/OSCAL/releases/tag/v1.3.0
```

The following schema files are relevant to this project:

| File | Purpose |
|------|---------|
| `oscal_assessment-results_schema.json` | Validate `telemetry/oscal-evidence/*.json` |
| `oscal_catalog_schema.json` | Validate control catalogs |
| `oscal_system-security-plan_schema.json` | Validate SSP documents |
| `oscal_plan-of-action-and-milestones_schema.json` | Validate POA&M documents |

## Usage

After downloading, place the schema files in this directory and run validation
using a tool such as [ajv-cli](https://github.com/ajv-validator/ajv-cli):

```bash
npx ajv validate \
  -s validation/oscal-1.3.0-schema/oscal_assessment-results_schema.json \
  -d telemetry/oscal-evidence/ac-2-evidence.json
```

Or use the Python [`jsonschema`](https://python-jsonschema.readthedocs.io/)
library:

```python
import json, jsonschema

with open("validation/oscal-1.3.0-schema/oscal_assessment-results_schema.json") as f:
    schema = json.load(f)

with open("telemetry/oscal-evidence/ac-2-evidence.json") as f:
    doc = json.load(f)

jsonschema.validate(doc, schema)
print("Validation passed.")
```

## FedRAMP Rev 5 Profile

The FedRAMP Moderate Rev 5 OSCAL profile is available at:

```
https://github.com/GSA/fedramp-automation/tree/master/dist/content/rev5/baselines
```
