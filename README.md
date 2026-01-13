# CSFLite Framework

*⚠️ Early development (WIP) — Expect changes to structure, mappings, and outputs.*

A lightweight NIST CSF v2.0 implementation for startups and SMEs that answers a simple question: do your foundational security capabilities exist at all?

---

## Vision

**CSFLite** is designed for lean security operations. Instead of overwhelming organizations with the full CSF catalog, this framework focuses on:

- The **Top 25 most impactful subcategories** across all CSF Functions
- What can be **automated** (e.g., open ports, outdated software, misconfigurations)
- What must be **validated manually** (e.g., policies, incident response plans, recovery strategies)

CSFLite takes a governance-first approach: a manual checklist assesses whether foundational capabilities exist before any attempt at maturity scoring, risk quantification, or control prescriptions.

---

## What's Included

### Framework Assets
- Curated CSFLite **subcategories** list (Top 25)
- Mapping of **Nuclei templates → CSF subcategories**
- CSV/JSON **lookup tables** for automation

### Tooling
- **Manual questionnaire** for governance assessment
- **Scripts** for processing questionnaire results and mapping scan outputs to CSF subcategories
- Example **Nuclei scan configurations** for common environments

### Templates & Guidance
- Suggested **remediation guidance**
- Example **policy, guides, and reporting templates**

---

## Use Case

This toolkit is for SMEs, startups, freelance consultants, and security-oriented DevOps teams who want structured risk insight without enterprise overhead.

---

## 🚀 Getting Started

Ready to run your first CSF assessment?

**→ [Get Started](docs/GETTING_STARTED.md)**

The Getting Started guide walks you through:
- Installing dependencies (Python, Poetry, Nuclei)
- Running a manual governance assessment workflow

---

## 📅 Roadmap

See [`doc/development_roadmap.md`](doc/development_roadmap.md) for phased deliverables and progress tracking.

---

## 📄 License

Released under the [MIT License](./LICENSE).

---

## 🙌 Contributions

Interested in contributing templates, fixes, or feedback? Please wait until the project reaches its first release milestone, then check the upcoming `CONTRIBUTING.md`.