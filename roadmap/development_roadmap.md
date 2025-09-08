# CSF-Lite Framework – Development Roadmap

This roadmap outlines the key phases and deliverables for building, validating, and publishing the CSF-Lite project. The framework combines lightweight NIST CSF v2.0 alignment with automated scanning and manual governance checks.

---

## ✅ Phase 1: Foundation – Define Scope & Priorities

**Deliverables:**
- [x] Identify Top 25 CSF subcategories
- [x] Classify which can be automated vs. manual
- [x] Draft lookup table and manual questionnaire

---

## Phase 2: Automate Core Functionality

**Deliverables:**
- [x] Build `csf_lookup.csv` and `csf_lookup.json`
- [x] Write `nuclei2csf.py` script to parse Nuclei JSON and output CSV with CSF mapping
- [x] Validate against a test scan output
- [x] Document automatable subcategories

---

## Phase 3: Manual Governance Checklist

**Deliverables:**
- [x] Write `manual_questionnaire.md` for non-scannable subcategories
- [x] Add `manual_remediation.md` for advisory follow-up

---

## Phase 4: Pilot Test

**Deliverables:**
- [ ] Run pilot scan + assessment on test environment
- [ ] Deliver full pilot CSFLite report (automated + manual)

---

## Phase 6: Community Growth & Iteration

**Deliverables:**
- [ ] Add CONTRIBUTING.md and issues templates
- [ ] Begin adding community-submitted templates and use cases
