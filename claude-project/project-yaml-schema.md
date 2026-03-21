# project.yaml — Schema Reference

This document defines the complete schema for Lean Security behavior specs. Claude uses this to validate specs before they're handed to Claude Code for execution.

---

## Top-Level Structure

```yaml
project:      # required — project identity
scope:        # required — what's in play
acceptance_criteria:  # required — how we know it's done
constraints:  # required — boundaries the agent must respect
deliverables: # required — what the project produces
stack:        # optional — which application scaffolds are needed
```

---

## project (required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Short identifier, kebab-case. Used in file naming and references. |
| domain | string | yes | Project category. Common values: `compliance`, `engineering`, `assessment`, `governance`. |
| description | string | yes | One-sentence description of what this project delivers. |

---

## scope (required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| target_framework | string | no | Compliance or regulatory framework if applicable. e.g. `SOC 2`, `HIPAA`, `ISO 27001`, `PCI DSS`. Omit for pure governance or engineering projects. |
| controls_in_scope | list[string] | yes | CSFLite control IDs that apply to this project. Use `["all"]` for full 25-control assessment. Every ID must exist in `csflite/controls.json`. |
| implementation_focus | list[object] | no | For engineering projects that build control implementations. Each entry defines a domain, its protocol files, and the controls it addresses. |

### implementation_focus entry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| domain | string | yes | Implementation domain. e.g. `edr`, `iam`, `backup`, `policy-as-code`. |
| protocols | list[string] | yes | Paths to protocol JSON files in `protocols/`. |
| controls | list[string] | yes | CSFLite control IDs this implementation addresses. |

---

## acceptance_criteria (required)

A list of strings. Each string is a verifiable statement that defines "done" for this project.

**Guidelines:**
- Machine-checkable criteria are preferred: "All control IDs validated against controls.json"
- Judgment criteria are acceptable but should be obvious: "Executive summary is under 2 pages"
- Avoid vague criteria: "Good quality" or "comprehensive" are not verifiable
- Each criterion should be independently testable

---

## constraints (required)

A list of strings. Each string is a non-functional requirement or boundary the agent must respect.

**Common constraints:**
- `"No maturity scoring — coverage only"` (always include this)
- `"All documents in markdown"`
- `"Client data never committed to repo"`
- `"Azure-only infrastructure"` (if applicable)
- `"Python 3.11+ required"` (if applicable)

---

## deliverables (required)

A list of objects. Each defines one output the project produces.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | yes | `doc` or `app` |
| subtype | string | yes | For docs: `gap-analysis`, `policy`, `mapping`, `assessment-report`, `executive-summary`. For apps: `cli`, `api`, `web`. |
| description | string | yes | What this deliverable is and who it's for. |

---

## stack (optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| cli | boolean | false | Whether a CLI application scaffold is needed. |
| api | boolean | false | Whether a FastAPI scaffold is needed. |
| frontend | boolean | false | Whether a React (Vite) frontend scaffold is needed. |

If any deliverable has `type: app`, the corresponding stack flags should be set. `web` subtype implies both `api: true` and `frontend: true`.

---

## Validation Rules

1. Every control ID in `controls_in_scope` and `implementation_focus.controls` must exist in `csflite/controls.json`
2. At least one acceptance criterion must be present
3. At least one constraint must be present (minimum: the no-maturity-scoring constraint)
4. At least one deliverable must be present
5. `project.name` must be kebab-case (lowercase, hyphens, no spaces)
6. If `deliverables` includes an `app` type, `stack` should be present with appropriate flags

---

## Complete Example

See `examples/baseline-assessment.yaml` for a fully worked example.
