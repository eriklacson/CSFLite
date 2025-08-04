# CSF-Lite Framework – Development Roadmap

This roadmap outlines the key phases and deliverables for building, validating, and publishing the CSF-Lite project. The framework combines lightweight NIST CSF v2.0 alignment with automated scanning and manual governance checks.

---

## ✅ Phase 1: Foundation – Define Scope & Priorities

**Deliverables:**
- [x] Identify Top 25 CSF subcategories
- [x] Classify which can be automated vs. manual
- [x] Draft lookup table and manual questionnaire

---

## 🚧 Phase 2: Automate Core Functionality

**Deliverables:**
- [ ] Build `csf_lookup.csv` and `csf_lookup.json`
- [ ] Write `map_to_csf.py` script to parse Nuclei JSON and output CSV with CSF mapping
- [ ] Validate against a test scan output
- [ ] Document automatable subcategories

---

## 🔍 Phase 3: Manual Governance Checklist

**Deliverables:**
- [x] Write `manual-questionnaire.md` for non-scanable subcategories
- [x] Add `manual-remediation.md` for advisory follow-up
- [ ] Create a standalone PDF/reporting version (optional)

---

## 🧪 Phase 4: Pilot Test

**Deliverables:**
- [ ] Run pilot scan + assessment on test environment
- [ ] Deliver full CSF-Lite report (automated + manual)
- [ ] Collect SME feedback and refine subcategory list and recommendations

---

## 📦 Phase 5: Package for GitHub

**Deliverables:**
- [ ] Finalize `README.md`, `LICENSE`, `.gitignore`
- [ ] Organize folders: `/docs`, `/tools`, `/templates`, `/data`
- [ ] Publish to GitHub under MIT or Apache 2.0
- [ ] (Optional) Add GitHub Project board for task tracking

---

## 🌱 Phase 6: Community Growth & Iteration

**Deliverables:**
- [ ] Add CONTRIBUTING.md and issues templates
- [ ] Announce project on LinkedIn, Reddit, or community groups
- [ ] Begin adding community-submitted templates and use cases
