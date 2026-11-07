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

## The Manual Governance Check

### The Question It Answers

The manual governance check exists to answer a simple, fundamental question:

> **Do the core cybersecurity outcomes exist at all?**

This is a simple assessment with three answers: Yes, Partial or No. It does not attempt to measure how well something works—only whether it exists in any intentional, repeatable form.

### What It Assesses

The manual governance check prioritizes **control coverage**, not exposure, likelihood, or business impact.

It intentionally assesses:

- **Existence**: Does a policy, process, plan, or practice exist?
- **Ownership**: Is accountability defined? Does someone own this outcome?
- **Scope**: Is the capability applied broadly, or only in isolated cases?
- **Documentation**: Is there evidence that this outcome is intentional rather than accidental?

### What It Intentionally Does Not Assess

The manual governance check does not attempt to measure:

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

These questions are unanswerable—or worse, produce false precision—when the organization has not established whether basic controls exist in any repeatable form.

This is the equivalent of asking calculus questions before arithmetic is solid.

### What "Coverage First" Means

CSFLite prioritizes establishing **what exists** before attempting to measure **how well it works** or **what happens if it fails**.

| Stage | Question | Output |
|-------|----------|--------|
| Coverage Assessment | Does this control exist? | Gap list |
| Maturity Assessment | How well does this control perform? | Maturity score |
| Risk Quantification | What is the likelihood and impact of failure? | Risk score |

CSFLite operates in Stage 1. It does not attempt Stage 2 or Stage 3.

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

CSFLite's manual governance check directly implements this emphasis. It assesses whether the organizational context, risk management strategy, roles, responsibilities, policies, and oversight mechanisms exist—exactly as GOVERN requires.

---

## The CSFLite Top 25 Subcategories

CSFLite does not attempt to assess all 106 CSF subcategories. Instead, it focuses on a curated subset of 25 high-impact subcategories selected for:

- **Foundational importance**: Controls that other controls depend on
- **Broad applicability**: Relevant to virtually all organizations regardless of sector
- **Assessability**: Can be meaningfully evaluated through a questionnaire and evidence review
- **Actionability**: Gaps can be addressed with clear, concrete steps

### Selection Criteria

The Top 25 were selected based on:

1. **Dependency analysis**: Which outcomes enable other outcomes?
2. **SME relevance**: Which outcomes matter most for small and mid-sized organizations?
3. **Governance criticality**: Which outcomes represent foundational governance capabilities?

### Distribution Across Functions

The Top 25 subcategories are distributed across all six CSF Functions to ensure balanced coverage:

| Function | Count | Focus Areas |
|----------|-------|-------------|
| GOVERN | 4 | Risk strategy, roles, policy, supply chain |
| IDENTIFY | 5 | Asset management, risk assessment |
| PROTECT | 6 | Access control, data security, platform security, resilience |
| DETECT | 4 | Continuous monitoring, adverse event analysis |
| RESPOND | 4 | Incident management, communication, mitigation |
| RECOVER | 2 | Recovery execution, communication |

This distribution ensures that CSFLite assessments do not over-index on any single aspect of cybersecurity.

---

## Guiding Principles

### 1. Coverage Before Depth

Establish what exists before measuring how well it works. Breadth of coverage enables meaningful prioritization.

### 2. Actionable Over Aspirational

Every assessment output should point to a concrete next step. Vague recommendations are not useful.

### 3. Defensible Over Precise

A clear Yes, Partial or No answer is more valuable than a nuanced score that cannot be explained or defended.

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

#### Assessment Method Basis

The procedural basis for governance evaluations is drawn from SP 800-53A Rev 5 (*Assessing Security and Privacy Controls in Information Systems and Organizations*). SP 800-53A Rev 5 defines three assessment methods that CSFLite governance checks are aligned to:

- **Examine** — Review of policies, procedures, plans, and documentation to confirm existence and scope
- **Interview** — Discussion with personnel to confirm that practices are understood and applied
- **Test** — Observation or verification that a capability is operational and repeatable

CSFLite governance questions rely mainly on the Examine and Interview methods. Test-based evidence (e.g., DR exercise records) is accepted as supporting documentation when cited by a respondent. It is not required for a "Yes", with one exception: backups, recovery procedures and the incident response plan, where a test is required (see the Evidence Rule). The full mapping of CSFLite subcategories to SP 800-53 Rev 5 controls and their applicable assessment methods is documented in [`docs/reference/csflite-800-53-crosswalk.md`](reference/csflite-800-53-crosswalk.md).

The questionnaire implements the coverage-first philosophy by asking existence-focused questions:

- "Does a documented [X] exist?"
- "Is responsibility for [X] assigned to a specific individual or role?"
- "Is [X] applied across the organization or only in specific areas?"

Questions avoid maturity language ("How mature is your...") and risk quantification ("What is the likelihood of...").

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

## Evidence-Based Scoring Requirements

### The Evidence Rule

**A "Yes" score means the outcome exists and evidence shows it. Assertions without evidence are scored "Partial" or "No".**

This is the most critical quality control mechanism in CSFLite assessments. Without evidence requirements, assessments devolve into attestation theater.

"Yes" does not mean the control works well. That would be a maturity question, and CSFLite does not ask it. In general, a test is not required.

**Exception: backups, recovery and incident response.** An untested backup is treated as no backup, because a backup that cannot be restored provides no recovery. The same holds for recovery procedures (RC.RP-01): a procedure that has never been run does not exist in any useful form. A "Yes" for backups (PR.DS-11) or recovery (RC.RP-01) requires evidence of a successful restoration or recovery test within the past 12 months. The same holds for the incident response plan (RS.MA-01): a plan that has never been exercised does not exist in any useful form. A "Yes" for the IR plan requires a tabletop exercise or drill report from the past 12 months. This exception applies only to these three. It is an existence check, not an effectiveness check.

The rule applies the same way whether the organization assesses itself or an outside person assesses it. A self-assessor must hold their own answers to the same standard. CSFLite does not verify evidence. Verification is the reviewer's job. The tool records the answer and the notes. A second reviewer is recommended for self-assessments.

**What the scores mean:**

- **Yes**: The outcome exists, has an owner, covers the stated scope, and evidence is provided.
- **Partial**: Something exists, but evidence is missing, or it covers only part of the scope, or it is documented but not applied.
- **No**: Nothing intentional and repeatable exists, or nothing can be shown.

### Scoring Decision Framework

| Organization Statement | Evidence Provided | Score | Rationale |
|-----------------|-------------------|-------|-----------|
| "We do backups" | Backup schedule, job logs, and a successful restoration test from the last 12 months | **Yes** | Backups exist and are shown to restore |
| "We do backups" | Backup schedule and job logs, no restoration test | **Partial** | Backups run but are not shown to restore |
| "We do backups" | Backup schedule documentation only | **Partial** | Practice is documented but not shown running |
| "We do backups" | No documentation | **No** | No evidence of intentional, repeatable practice |
| "We have an IR plan" | Approved plan with owner, version and date, plus a tabletop or drill report from the last 12 months | **Yes** | Plan exists, is owned, and has been exercised |
| "We have an IR plan" | Approved plan with owner, version and date, no exercise | **Partial** | Plan is adopted but not shown to work |
| "We have an IR plan" | Draft or unapproved plan | **Partial** | Plan is written but not adopted |
| "We enforce MFA" | Screenshot showing MFA required for all accounts | **Yes** | Technical enforcement visible |
| "We enforce MFA" | Policy document requiring MFA | **Partial** | Policy exists, no proof of enforcement |

### Evidence Quality Standards

Acceptable evidence must meet three criteria:

#### 1. Current
- **Dated records** (job logs, review minutes, exercise reports): within the past 12 months
- **Configuration controls:** Current screenshots or exports (not outdated)
- **Policy controls:** Latest approved version with effective date

#### 2. Specific
- Shows the control is in place, not only described
- Demonstrates scope (all systems, all users, all locations)

#### 3. Verifiable
- Can be independently confirmed if needed
- Contains sufficient detail to assess completeness
- Not generic templates or aspirational documents

### Examples by Control Type

#### Governance Controls (GV.*)

**Acceptable evidence:**
- Policy documents with approval signatures and effective dates
- Organizational charts showing security ownership
- Meeting minutes documenting risk decisions
- Approved risk appetite statements

**Insufficient evidence:**
- Draft policies not yet approved
- Informal email threads about responsibilities
- Generic policy templates without customization

#### Asset Management (ID.AM-*)

**Acceptable evidence:**
- Current asset inventory (spreadsheet, CMDB export)
- Network discovery scan results
- Asset classification matrix with ownership
- Software inventory with version tracking

**Insufficient evidence:**
- Outdated inventory (older than 12 months)
- Incomplete inventory missing significant systems
- No ownership or classification metadata

#### Access Control (PR.AA-*)

**Acceptable evidence:**
- IAM policy exports showing configurations
- Screenshots of MFA enforcement settings
- Access control matrices (role-permission mappings)
- User provisioning/deprovisioning logs

**Insufficient evidence:**
- Policy documents describing desired state
- Partial MFA deployment (admin only)
- No evidence of enforcement mechanisms

#### Data Protection (PR.DS-*)

**Acceptable evidence:**
- Encryption configuration screenshots (S3, RDS, disk)
- TLS/SSL certificate details and cipher suites
- Backup job logs plus a dated restoration test result (within 12 months)
- Data classification scheme with handling requirements

**Insufficient evidence:**
- Statement that "encryption is enabled"
- Backup schedules or job logs with no restoration test

#### Detection & Monitoring (DE.*)

**Acceptable evidence:**
- Log retention configuration (CloudTrail, Splunk, etc.)
- Alert rule definitions with thresholds
- SIEM dashboard screenshots showing coverage
- Sample security event logs

**Insufficient evidence:**
- Basic logging with no monitoring or alerting
- Alerts configured but no evidence of triage
- No log retention or analysis capability

#### Incident Response (RS.*)

**Acceptable evidence:**
- IR plan document with version control
- Tabletop exercise or drill report (within 12 months)
- Incident communication templates
- Post-incident review documentation

**Insufficient evidence:**
- Draft or unapproved IR plan
- Approved IR plan with no exercise or drill report
- Generic IR templates without customization
- No evidence of organizational awareness

### When Evidence is Unavailable

If an organization cannot provide evidence:

**Scenario 1: Control is documented but not enforced**
- **Score:** Partial
- **Example:** Password policy exists but no technical enforcement
- **Rationale:** Intent exists but not operationalized

**Scenario 2: Control exists informally but not documented**
- **Score:** No, unless some records show it runs (then Partial)
- **Example:** "We do backups but don't document them"
- **Rationale:** Cannot distinguish intentional practice from accident

**Scenario 3: Control cannot be demonstrated**
- **Score:** No
- **Example:** "We have monitoring but can't show configurations"
- **Rationale:** Indistinguishable from non-existent

**Scenario 4: Control is under construction**
- **Score:** No
- **Example:** "We're implementing MFA next month"
- **Rationale:** Coverage assessment reflects current state, not future intent

### Reviewer Guidance

A reviewer is the outside assessor, or the person on the team who checks the answers.

**When an organization claims a control exists:**

1. **Request specific evidence:** "Can you show me [artifact]?"
2. **Verify currency:** "When was this last updated or reviewed?"
3. **Check scope:** "Does this cover all [systems/users/locations]?"
4. **Confirm enforcement:** "How do you verify this is being followed?"

**If the organization hesitates or cannot provide evidence:**

- Explain that "Yes" requires evidence, not trust
- Offer to score as "Partial" if documentation exists
- Note the gap in assessment findings
- Recommend evidence collection as remediation step

**Never:**
- Accept verbal assertions alone as evidence. Interview answers give context. They can support a score but cannot earn a "Yes" without an artifact
- Assume controls exist based on industry norms
- Score aspirational or planned controls as current
- Compromise evidence requirements to avoid difficult conversations

### Quality Control Checkpoint

Before finalizing any assessment, verify:

- [ ] Every "Yes" score has documented evidence in assessment notes
- [ ] Evidence meets currency standards (dated records within 12 months)
- [ ] Evidence is specific (not generic templates)
- [ ] Partial/No scores have clear gap explanations
- [ ] No scores are based solely on organization assertions

---

## Scoring and Weighting

### The Scoring Model

CSFLite uses a weighted scoring model that:

- Assigns each subcategory a weight based on its relative importance
- Produces a weighted score and gap score for each subcategory
- Orders gaps by gap score. Weight sets the order. There is no per-organization adjustment.
- Severity reflects coverage only (Yes = none, Partial = medium, No = high); weight sets priority through the gap score

### What Scores Represent

CSFLite scores represent **coverage**, not maturity or risk.

A coverage score of 80% means: "the responses earn 80% of the total weight." Weight is how much each outcome counts.

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

CSFLite does not calculate risk scores, estimate breach probabilities, or model financial impact. These activities require a baseline of existing controls—exactly what CSFLite helps establish.

### Not a Maturity Model

CSFLite does not assess control maturity. It does not distinguish between "initial," "managed," "defined," "quantitatively managed," and "optimizing" capability levels. It asks only: "Does this exist?"

### Not a Replacement for Professional Assessment

CSFLite is a self-assessment tool, which an outside reviewer can also use. It is designed for organizations that cannot afford or do not yet need professional security consulting. It does not replace penetration testing, security architecture review, or expert risk assessment.

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
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Stage 1: Coverage Assessment (CSFLite)                     │
│  ───────────────────────────────────────                    │
│  Question: Do controls exist?                               │
│  Output: Gap list, coverage scores                          │
│  Audience: Any organization                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 2: Maturity Assessment                               │
│  ────────────────────────────                               │
│  Question: How well do controls perform?                    │
│  Output: Maturity levels, improvement roadmap               │
│  Prerequisite: Stage 1 complete                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 3: Risk Quantification                               │
│  ─────────────────────────                                  │
│  Question: What is the likelihood and impact of failure?    │
│  Output: Risk scores, prioritized risk register             │
│  Prerequisite: Stages 1 and 2 complete                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 4: Continuous Risk Management                        │
│  ───────────────────────────────────────                    │
│  Question: How is risk changing over time?                  │
│  Output: Trend analysis, real-time risk posture             │
│  Prerequisite: Stages 1, 2, and 3 complete                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Organizations should not attempt later stages until earlier stages are complete. CSFLite provides the foundation.

Before you can measure control effectiveness, you must have controls.  
Before you can quantify risk, you must know what you're protecting.  
Before you can achieve compliance, you must have something to certify.

CSFLite provides the foundation. What organizations build on that foundation is up to them.

---

## Summary

CSFLite operates on a simple premise: **coverage precedes everything else**.

It asks whether foundational security outcomes exist before attempting to measure maturity, quantify risk, or claim compliance.

This is not a limitation. It is a deliberate design that prioritizes:

- Defensible assessments over subjective scoring
- Actionable gaps over theoretical risk models
- Organizational clarity over security theater

CSFLite works because it respects the constraints of small and mid-sized teams while producing outputs that scale as organizations grow.

---

## Document Metadata

| Field | Value |
|-------|-------|
| Version | 1.1 |
| Last Updated | 2026-11-07 |
| Status | Active |
| Authoritative | Yes |

This document governs all CSFLite assessment methodology decisions. Conflicts between this document and other CSFLite documentation should be resolved in favor of this document.
