# CSFLite Assessment Philosophy

## Purpose of This Document

This document defines the philosophical foundation and design rationale for CSFLite's assessment methodology. It serves as the authoritative reference for understanding why CSFLite operates the way it does and ensures consistency across all framework components, documentation, and tooling.

---

## Core Thesis

**You cannot measure what does not exist.**

Traditional cybersecurity risk frameworks assume controls are in place and ask: *"How well are they working?"*

CSFLite asks the prior question: *"Do they exist at all?"*

This is not a simplification. It is a deliberate resequencing of how cybersecurity capability is assessed in resource-constrained organizations.

---

## The Separation of Automated and Manual Assessment

CSFLite deliberately separates automated technical scanning from manual governance checks. This is a design decision, not a limitation.

### What Automated Scanning Can Do

Automated tools (such as Nuclei vulnerability scanners) are effective at identifying technical signals:

- Exposed services and open ports
- Outdated software and missing patches
- Misconfigurations and insecure defaults
- Known vulnerabilities (CVEs)
- Weak cryptographic implementations

These are observable, repeatable, and machine-verifiable.

### What Automated Scanning Cannot Do

Automated tools cannot determine whether an organization has the foundational governance capabilities required to sustain cybersecurity over time:

- Whether a policy exists
- Whether ownership and accountability are defined
- Whether a process is documented and followed
- Whether personnel are trained
- Whether incident response has been planned
- Whether recovery capabilities have been tested

These require human judgment and organizational context.

### Why Both Are Required

A vulnerability scan can tell you that port 22 is exposed. It cannot tell you whether anyone is responsible for reviewing SSH access, whether there is a policy governing remote access, or whether the organization would know what to do if that access were compromised.

CSFLite combines both tracks to produce a complete picture:

| Track | What It Assesses | Method |
|-------|------------------|--------|
| Automated | Technical exposure signals | Nuclei scans mapped to CSF subcategories |
| Manual | Governance capability existence | Structured questionnaire responses |

Neither track alone is sufficient. Together, they produce an actionable baseline.

---

## The Manual Governance Check

### The Question It Answers

The manual governance check exists to answer a simple, fundamental question:

> **Do the core cybersecurity outcomes exist at all?**

This is a binary or near-binary assessment. It does not attempt to measure how well something worksâ€”only whether it exists in any intentional, repeatable form.

### What It Assesses

The manual governance phase prioritizes **control coverage**, not exposure, likelihood, or business impact.

It intentionally assesses:

- **Existence**: Does a policy, process, plan, or practice exist?
- **Ownership**: Is accountability defined? Does someone own this outcome?
- **Scope**: Is the capability applied broadly, or only in isolated cases?
- **Documentation**: Is there evidence that this outcome is intentional rather than accidental?

### What It Intentionally Does Not Assess

The manual governance phase does not attempt to measure:

- **Control effectiveness or maturity**: How well does this control perform?
- **Threat likelihood**: How probable is exploitation?
- **Exploit probability**: What is the technical attack surface?
- **Financial impact**: What would a failure cost?
- **Risk quantification**: What is the calculated risk score?

These analyses assume a baseline that many small teams and SMEs have not yet established.

### The Rationale

CSFLite takes the position that it is neither accurate nor useful to model exposure or impact for controls that do not exist in a repeatable or intentional way.

Calculating the "likelihood of incident response failure" is meaningless if no incident response plan exists. Estimating "data breach impact" is theatrical if no one knows what data the organization holds or where it resides.

Coverage must come first.

---

## Coverage First, Not Risk First

### The Sequencing Problem

For small and mid-sized organizations, cybersecurity risk conversations often fail because they start too far downstream:

- "What is your risk appetite?"
- "What is the likelihood of a breach?"
- "What is the financial impact of this threat scenario?"

These questions are unanswerableâ€”or worse, produce false precisionâ€”when the organization has not established whether basic controls exist in any repeatable form.

This is the equivalent of asking calculus questions before arithmetic is solid.

### What "Coverage First" Means

CSFLite prioritizes establishing **what exists** before attempting to measure **how well it works** or **what happens if it fails**.

| Phase | Question | Output |
|-------|----------|--------|
| Coverage Assessment | Does this control exist? | Gap list |
| Maturity Assessment | How well does this control perform? | Maturity score |
| Risk Quantification | What is the likelihood and impact of failure? | Risk score |

CSFLite operates in Phase 1. It does not attempt Phase 2 or Phase 3.

### Why This Works for SMEs and Lean Teams

Small teams do not have security specialists who can defend nuanced maturity scores or risk quantification models. But they can answer:

- "Do we have a documented incident response plan?" Yes or no.
- "Is there an asset inventory?" Yes or no.
- "Has anyone been assigned responsibility for security?" Yes or no.

These answers are defensible. They produce actionable gap lists. They enable leadership to make decisions without security specialization.

By prioritizing coverage:

- **Gaps become obvious and defensible**: The organization either has a backup policy or it does not.
- **Priorities become actionable**: Fix what is missing, not what scores poorly on a subjective scale.
- **Leadership can make decisions**: No specialized security knowledge required to understand "we don't have an incident response plan."

---

## Alignment with NIST CSF v2.0

CSFLite's coverage-first approach aligns with the NIST Cybersecurity Framework v2.0 philosophy.

### CSF Core Structure

The NIST CSF Core is organized as:

- **Functions**: GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER
- **Categories**: Groups of related cybersecurity outcomes within each Function
- **Subcategories**: Specific outcomes of technical and management activities

The CSF explicitly states that these outcomes are "not a checklist of actions to perform" and that "specific actions taken to achieve an outcome will vary by organization."

### Outcome-Based, Not Control-Based

The CSF describes **desired outcomes**, not prescriptive controls. This is intentional. It allows organizations to achieve outcomes through whatever means are appropriate to their context.

CSFLite preserves this philosophy by asking: "Is this outcome being achieved?" rather than "Are you using this specific control?"

### The GOVERN Function

CSF v2.0 added the GOVERN Function to emphasize that governance activities are critical for incorporating cybersecurity into an organization's broader enterprise risk management strategy.

CSFLite's manual governance check directly implements this emphasis. It assesses whether the organizational context, risk management strategy, roles, responsibilities, policies, and oversight mechanisms existâ€”exactly as GOVERN requires.

---

## The CSFLite Top 25 Subcategories

CSFLite does not attempt to assess all 106 CSF subcategories. Instead, it focuses on a curated subset of 25 high-impact subcategories selected for:

- **Foundational importance**: Controls that other controls depend on
- **Broad applicability**: Relevant to virtually all organizations regardless of sector
- **Assessability**: Can be meaningfully evaluated through scanning or questionnaire
- **Actionability**: Gaps can be addressed with clear, concrete steps

### Selection Criteria

The Top 25 were selected based on:

1. **Dependency analysis**: Which outcomes enable other outcomes?
2. **SME relevance**: Which outcomes matter most for small and mid-sized organizations?
3. **Automation potential**: Which outcomes can be partially assessed through scanning?
4. **Governance criticality**: Which outcomes represent foundational governance capabilities?

### Distribution Across Functions

The Top 25 subcategories are distributed across all six CSF Functions to ensure balanced coverage:

| Function | Count | Focus Areas |
|----------|-------|-------------|
| GOVERN | 5 | Risk strategy, roles, policy, oversight, supply chain |
| IDENTIFY | 5 | Asset management, risk assessment, improvement |
| PROTECT | 7 | Access control, awareness, data security, platform security |
| DETECT | 3 | Continuous monitoring, adverse event analysis |
| RESPOND | 3 | Incident management, analysis, mitigation |
| RECOVER | 2 | Recovery execution, communication |

This distribution ensures that CSFLite assessments do not over-index on any single aspect of cybersecurity.

---

## Scoring and Weighting

### The Scoring Model

CSFLite uses a weighted scoring model that:

- Assigns each subcategory a weight based on its relative importance
- Produces scores at the subcategory, category, and function levels
- Generates an overall framework score

### What Scores Represent

CSFLite scores represent **coverage**, not maturity or risk.

A score of 80% means: "80% of the assessed outcomes exist in some intentional form."

It does not mean: "The organization has achieved 80% of possible cybersecurity maturity" or "80% of cybersecurity risks are mitigated."

### Appropriate Use of Scores

Scores are useful for:

- Tracking progress over time within the same organization
- Identifying which Functions or Categories have the largest gaps
- Communicating coverage status to leadership in aggregate form

Scores are not useful for:

- Comparing organizations against each other
- Claiming compliance with any standard or regulation
- Representing overall cybersecurity "health" or "risk posture"

---

## What CSFLite Is Not

### Not a Compliance Framework

CSFLite is not a compliance framework. It does not certify that an organization meets any regulatory requirement. It does not produce audit-ready evidence packages. It does not replace SOC 2, ISO 27001, HIPAA, PCI-DSS, or any other compliance program.

### Not a Risk Quantification Tool

CSFLite does not calculate risk scores, estimate breach probabilities, or model financial impact. These activities require a baseline of existing controlsâ€”exactly what CSFLite helps establish.

### Not a Maturity Model

CSFLite does not assess control maturity. It does not distinguish between "initial," "managed," "defined," "quantitatively managed," and "optimizing" capability levels. It asks only: "Does this exist?"

### Not a Replacement for Professional Assessment

CSFLite is a self-assessment tool designed for organizations that cannot afford or do not yet need professional security consulting. It does not replace penetration testing, security architecture review, or expert risk assessment.

---

## When to Go Deeper

CSFLite is intentionally designed as a **baseline assessment framework**.

Once coverage is established and governance capabilities are in place, organizations may choose to layer in:

- **Threat modeling**: Identifying specific threats relevant to the organization
- **Risk quantification**: Calculating likelihood and impact of identified risks
- **Financial impact analysis**: Estimating costs of potential incidents
- **Control effectiveness testing**: Measuring how well controls actually perform
- **Continuous control monitoring**: Ongoing validation of control operation
- **Maturity assessment**: Evaluating the sophistication of existing controls

CSFLite does not replace these practices. It ensures they are built on solid ground.

### The Progression Model

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                                                                 â”‚
â”‚  Stage 1: Coverage Assessment (CSFLite)                        â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€                         â”‚
â”‚  Question: Do controls exist?                                   â”‚
â”‚  Output: Gap list, coverage scores                              â”‚
â”‚  Audience: Any organization                                     â”‚
â”‚                                                                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                 â”‚
â”‚  Stage 2: Maturity Assessment                                   â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€                                   â”‚
â”‚  Question: How well do controls perform?                        â”‚
â”‚  Output: Maturity levels, improvement roadmap                   â”‚
â”‚  Prerequisite: Stage 1 complete                                 â”‚
â”‚                                                                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                 â”‚
â”‚  Stage 3: Risk Quantification                                   â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€                                    â”‚
â”‚  Question: What is the likelihood and impact of failure?        â”‚
â”‚  Output: Risk scores, prioritized risk register                 â”‚
â”‚  Prerequisite: Stages 1 and 2 complete                          â”‚
â”‚                                                                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                 â”‚
â”‚  Stage 4: Continuous Risk Management                            â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€                            â”‚
â”‚  Question: How is risk changing over time?                      â”‚
â”‚  Output: Trend analysis, real-time risk posture                 â”‚
â”‚  Prerequisite: Stages 1, 2, and 3 complete                      â”‚
â”‚                                                                 â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Organizations should not attempt later stages until earlier stages are complete. CSFLite provides the foundation.

---

## Guiding Principles

### 1. Coverage Before Depth

Establish what exists before measuring how well it works. Breadth of coverage enables meaningful prioritization.

### 2. Actionable Over Aspirational

Every assessment output should point to a concrete next step. Vague recommendations are not useful.

### 3. Defensible Over Precise

A clear "yes/no" answer is more valuable than a nuanced score that cannot be explained or defended.

### 4. Governance as Infrastructure

Treat governance capabilities (policies, ownership, processes) as foundational infrastructure, not bureaucratic overhead.

### 5. Compliance as Output, Not Driver

Good security practices produce compliance as a byproduct. Chasing compliance checkboxes does not produce good security.

### 6. Lean by Default

Minimize overhead. Every artifact, process, and assessment activity should justify its existence.

### 7. Startup-First Design

Design for resource-constrained organizations. If it doesn't work for a 10-person team, it doesn't belong in CSFLite.

---

## Application to CSFLite Components

### Manual Governance Questionnaire

The questionnaire implements the coverage-first philosophy by asking existence-focused questions:

- "Does a documented [X] exist?"
- "Is responsibility for [X] assigned to a specific individual or role?"
- "Is [X] applied across the organization or only in specific areas?"

Questions avoid maturity language ("How mature is your...") and risk quantification ("What is the likelihood of...").

### Automated Scan Processing

Nuclei scan results are mapped to CSF subcategories to identify technical coverage gaps. The mapping focuses on:

- Which technical controls are demonstrably in place (or absent)
- Which outcomes have observable evidence

Scan results do not produce risk scores or threat assessments.

### Assessment Reports

Reports produced by CSFLite tooling focus on:

- What exists vs. what is missing (coverage)
- Prioritized gaps based on subcategory weighting
- Concrete next steps for addressing gaps

Reports avoid:

- Risk scores or risk ratings
- Maturity levels or maturity curves
- Compliance claims or certification language

### Remediation Guidance

Remediation guidance is:

- Specific and actionable
- Scaled to SME resources and capabilities
- Focused on establishing existence, not optimizing performance

---

## Summary

CSFLite operates on a simple premise: **coverage precedes everything else**.

Before you can measure control effectiveness, you must have controls.
Before you can quantify risk, you must know what you're protecting.
Before you can achieve compliance, you must have something to certify.

CSFLite provides the foundation. What organizations build on that foundation is up to them.

---

## Document Metadata

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Last Updated | 2025-01-13 |
| Status | Active |
| Authoritative | Yes |

This document governs all CSFLite assessment methodology decisions. Conflicts between this document and other CSFLite documentation should be resolved in favor of this document.