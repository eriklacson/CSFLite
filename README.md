# CSFLite Framework

A practical, lightweight implementation of the NIST Cybersecurity Framework (CSF v2.0) for small tech teams, startups, and SMEs. Combines automation tools with manual governance checks to produce a fast, actionable security baseline.

---

## Vision

**CSFLite** is designed for lean security operations. Instead of overwhelming organizations with the full CSF catalog, this framework focuses on:

- The **Top 25 most impactful subcategories** across all CSF Functions
- What can be **automated** (e.g., open ports, outdated software, misconfigurations)
- What must be **validated manually** (e.g., policies, incident response plans, recovery strategies)

---

## What's Included

This repository contains:

- ✅ Curated CSFLite **subcategories** list (top 25)
- ✅ A **manual questionnaire** for governance assessment
- ✅ A **script** for processing the governance questionnaire results
- ✅ Mapping of **Nuclei templates → CSF subcategories**
- ✅ CSV/JSON **lookup tables** for automation
- ✅ Suggested **remediation guidance**
- ✅ Example **policy, guides and reporting templates**
- ✅ Python scripts for mappping scan outputs and manual questioinaire results to CSF subcategories.
- ✅ Example **Nuclei scan configurations** for common environments

---

## 🚀 Getting Started

Ready to run your first CSF assessment?

**→ [Get Started in 10 Minutes](docs/GETTING_STARTED.md)**

The Getting Started guide walks you through:
- Installing dependencies (Python, Poetry, Nuclei)
- Running a manual governance assessment worklfow

---

## Use Case

This toolkit is for:

- **SMEs/startups** that want structured risk insight without enterprise overhead
- **Freelancers/consultants** running lightweight assessments
- **Security-oriented DevOps teams** bridging scanning and policy gaps

---

## Status

**This project is currently in early development (WIP).**  
Expect changes to structure, mappings, and outputs.  
Contributors are welcome once the first working release is finalized.

---

## 📅 Roadmap

See [`roadmap/development-roadmap.md`](doc/development_roadmap.md) for phased deliverables and progress tracking.

---

## 📄 License

Released under the [MIT License](./LICENSE).

---

## 🙌 Contributions

Interested in contributing templates, fixes, or feedback? Please wait until the project reaches its first release milestone, then check the upcoming `CONTRIBUTING.md`.
