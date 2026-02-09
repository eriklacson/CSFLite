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

This is a binary or near-binary assessment. It does not attempt to measure how well something works—only whether it exists in any intentional, repeatable form.

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

These questions are unanswerable—or worse, produce false precision—when the organization has not established whether basic controls exist in any repeatable form.

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

CSFLite's manual governance check directly implements this emphasis. It assesses whether the organizational context, risk management strategy, roles, responsibilities, policies, and oversight mechanisms exist—exactly as GOVERN requires.

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

## Evidence-Based Scoring Requirements

### The Evidence Rule

**A "Yes" score requires supporting evidence. Assertions without proof are scored "Partial" or "No".**

This is the most critical quality control mechanism in CSFLite assessments. Without evidence requirements, assessments devolve into attestation theater where organizations self-report compliance without verification.

### Scoring Decision Framework

| Client Statement | Evidence Provided | Score | Rationale |
|-----------------|-------------------|-------|-----------|
| "We do backups" | Last 3 restoration test reports | **Yes** | Control exists, enforced, and tested |
| "We do backups" | Backup schedule documentation only | **Partial** | Control exists but not validated |
| "We do backups" | No documentation | **No** | No evidence of intentional, repeatable practice |
| "We have an IR plan" | Plan document + tabletop exercise report from last 6 months | **Yes** | Control exists and has been tested |
| "We have an IR plan" | Plan document, untested | **Partial** | Control documented but not validated |
| "We enforce MFA" | Screenshot showing MFA required for all accounts | **Yes** | Technical enforcement visible |
| "We enforce MFA" | Policy document requiring MFA | **Partial** | Policy exists, no proof of enforcement |

### Evidence Quality Standards

Acceptable evidence must meet three criteria:

#### 1. Current
- **Tested controls:** Evidence within past 12 months (backups, DR, IR plans)
- **Configuration controls:** Current screenshots or exports (not outdated)
- **Policy controls:** Latest approved version with effective date

#### 2. Specific
- Shows the control in operation, not just existence
- Demonstrates scope (all systems, all users, all locations)
- Includes validation or testing results where applicable

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
- Outdated inventory (>6 months old)
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
- Backup restoration test results with dates
- Data classification scheme with handling requirements

**Insufficient evidence:**
- Statement that "encryption is enabled"
- Backup schedules without test results
- No evidence of immutable or offline backups

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
- Tabletop exercise reports (last 12 months)
- Incident communication templates
- Post-incident review documentation

**Insufficient evidence:**
- IR plan that has never been tested
- Generic IR templates without customization
- No evidence of organizational awareness

### When Evidence is Unavailable

If a client cannot provide evidence:

**Scenario 1: Control is documented but not enforced**
- **Score:** Partial
- **Example:** Password policy exists but no technical enforcement
- **Rationale:** Intent exists but not operationalized

**Scenario 2: Control exists informally but not documented**
- **Score:** Partial (at best) or No
- **Example:** "We do backups but don't document or test them"
- **Rationale:** Cannot distinguish intentional practice from accident

**Scenario 3: Control cannot be demonstrated**
- **Score:** No
- **Example:** "We have monitoring but can't show configurations"
- **Rationale:** Indistinguishable from non-existent

**Scenario 4: Control is under construction**
- **Score:** No
- **Example:** "We're implementing MFA next month"
- **Rationale:** Coverage assessment reflects current state, not future intent

### Assessor Guidance

**When a client claims a control exists:**

1. **Request specific evidence:** "Can you show me [artifact]?"
2. **Verify currency:** "When was this last updated/tested?"
3. **Check scope:** "Does this cover all [systems/users/locations]?"
4. **Confirm enforcement:** "How do you verify this is being followed?"

**If client hesitates or cannot provide evidence:**

- Explain that "Yes" requires proof, not trust
- Offer to score as "Partial" if documentation exists
- Note the gap in assessment findings
- Recommend evidence collection as remediation step

**Never:**
- Accept verbal assertions as evidence
- Assume controls exist based on industry norms
- Score aspirational or planned controls as current
- Compromise evidence requirements to avoid difficult conversations

### Quality Control Checkpoint

Before finalizing any assessment, verify:

- [ ] Every "Yes" score has documented evidence in assessment notes
- [ ] Evidence meets currency standards (tested controls within 12 months)
- [ ] Evidence is specific (not generic templates)
- [ ] Partial/No scores have clear gap explanations
- [ ] No scores are based solely on client assertions

---

## Contextual Prioritization

### Beyond Framework Weights

CSFLite framework weights (stored in `data/csf_lookup.csv`) reflect general importance across organizations. However, **gap priority must be adjusted for each client's specific risk profile.**

Framework weights answer: "Which controls matter most in general?"

Context multipliers answer: "Which gaps matter most for THIS organization?"

### The Problem with Generic Prioritization

**Without context adjustment:**

A cloud-only SaaS company and an on-premise healthcare provider would receive identical gap prioritization:

| Gap | Framework Weight | Generic Priority |
|-----|-----------------|-----------------|
| Physical access controls | 1.25 | Medium |
| Vulnerability management | 1.50 | High |
| Incident response plan | 1.50 | High |

**But their actual priorities differ significantly:**

| Gap | SaaS Company | Healthcare Provider |
|-----|--------------|-------------------|
| Physical access controls | **Low** (no data centers) | **High** (server rooms, medical devices) |
| Vulnerability management | **Critical** (public attack surface) | **Medium** (limited external exposure) |
| Incident response plan | **High** (customer trust) | **Critical** (HIPAA requirements) |

Context-adjusted prioritization ensures assessments drive action on gaps that actually matter.

### Gathering Threat Context

Before calculating final gap priorities, assessors must gather:

#### 1. Data Sensitivity

**Question:** What types of data does the organization handle?

**Options:**
- Customer PII (names, emails, addresses, phone numbers)
- Payment information (credit cards, bank accounts)
- Health records or medical information
- Government-issued IDs or sensitive credentials
- Proprietary business data (trade secrets, source code, financials)
- Employee data (HR records, compensation)
- Third-party data processed on behalf of customers
- Minimal sensitive data

**Use:** Determines data protection control priority

---

#### 2. Infrastructure Model

**Question:** Where does the organization's infrastructure run?

**Options:**
- Cloud-only (AWS, GCP, Azure, managed SaaS)
- Hybrid (cloud + on-premise)
- On-premise only
- Primarily third-party SaaS tools

**Use:** Determines physical security, network segmentation, cloud control priorities

---

#### 3. Compliance Pressure

**Question:** What compliance requirements apply?

**Options:**
- Customer contractual requirements (SOC 2, ISO 27001 questionnaires)
- Data protection regulations (GDPR, CCPA, Philippine DPA)
- Industry-specific (PCI-DSS, HIPAA, financial regulations)
- None currently
- Upcoming in next 6-12 months

**Follow-up:** Timeline pressure? (e.g., "Customer requires SOC 2 by Q3")

**Use:** Determines governance control priority, may increase urgency of specific gaps

---

#### 4. Threat Profile

**Question:** Who would want to target this organization?

**Options:**
- Opportunistic bots / automated attacks (credential stuffing, vulnerability scanning)
- Financially motivated attackers (ransomware, fraud, data theft for resale)
- Competitors seeking proprietary information
- Disgruntled or negligent insiders
- Nation-state actors or advanced persistent threats
- Ideologically motivated groups
- Unknown / haven't considered

**Use:** Determines detection, monitoring, access control priorities

---

#### 5. Business Model & Exposure

**Question:** How does the organization operate?

**Options:**
- B2B SaaS (software service to businesses)
- B2C marketplace or platform
- Enterprise software (on-premise or private cloud)
- Professional services / consulting
- E-commerce or retail

**Follow-up:** Public-facing services? Customer-facing applications?

**Use:** Determines attack surface, vulnerability management priority

---

### Context Multiplier Application

After calculating base gap scores using `governance_check.py`, apply context multipliers:

```
adjusted_gap_score = base_gap_score × context_multiplier
```

**Context Multiplier Range:** 0.5x to 2.0x

#### Increase Priority (1.5x - 2.0x)

Apply higher multipliers when:

| Scenario | Multiplier | Example |
|----------|-----------|---------|
| Control protects high-sensitivity data client handles | 1.5x | B2B SaaS handling customer PII + IAM gap |
| Gap directly blocks stated compliance requirement | 1.8x - 2.0x | SOC 2 deadline + governance gap |
| Client has public-facing services (attack surface) | 1.5x | SaaS product + vulnerability management gap |
| Client operates in regulated industry | 1.5x | Healthcare + data protection gap |
| Client has experienced related incidents | 1.8x | Past breach + monitoring gap |

#### Normal Priority (1.0x)

Apply standard multiplier when:
- Standard applicability
- No specific heightened risk factors
- General importance but not client-specific urgency

#### Decrease Priority (0.5x - 0.75x)

Apply lower multipliers when:

| Scenario | Multiplier | Example |
|----------|-----------|---------|
| Control addresses threat client doesn't face | 0.5x | Cloud-only + physical security gap |
| Industry-specific control, client in different industry | 0.6x | Healthcare-specific + fintech client |
| Client has strong compensating controls | 0.7x | Limited vendors + supply chain risk |
| Legacy concern, not current threat vector | 0.6x | Floppy disk encryption for cloud startup |

### Practical Examples

#### Example 1: B2B SaaS Company

**Client Profile:**
- B2B SaaS platform (project management software)
- Handles customer PII and business data
- Cloud-only (AWS infrastructure)
- No compliance requirements yet, customers starting to ask
- 50 employees, no security team

**Context Adjustments:**

| Gap | Base Score | Reasoning | Multiplier | Adjusted Score |
|-----|------------|-----------|------------|----------------|
| **ID.RA-01** Vulnerability management | 1.50 | Public SaaS = high attack surface | **1.5x** | **2.25** |
| **PR.AA-01** IAM | 1.50 | Customer data access = critical | **1.5x** | **2.25** |
| **DE.CM-01** Network monitoring | 1.25 | SaaS uptime = revenue | **1.5x** | **1.88** |
| **GV.RM-01** Risk management | 1.50 | Standard importance | **1.0x** | **1.50** |
| **RS.MA-01** Incident response | 1.50 | Customer trust dependency | **1.3x** | **1.95** |
| **PR.AC-07** Physical security | 1.25 | Cloud-only, no data centers | **0.5x** | **0.63** |

**Top 3 Adjusted Gaps:**
1. ID.RA-01 (2.25) - Vuln mgmt critical for public services
2. PR.AA-01 (2.25) - IAM prevents unauthorized data access
3. RS.MA-01 (1.95) - IR plan protects customer relationships

---

#### Example 2: Healthcare Clinic

**Client Profile:**
- Medical clinic with electronic health records (EHR)
- Handles protected health information (PHI)
- Hybrid infrastructure (on-premise servers + cloud EHR)
- HIPAA compliance required
- 80 employees including clinical and admin staff

**Context Adjustments:**

| Gap | Base Score | Reasoning | Multiplier | Adjusted Score |
|-----|------------|-----------|------------|----------------|
| **PR.DS-01** Data-at-rest encryption | 1.00 | PHI = mandatory encryption | **2.0x** | **2.00** |
| **GV.PO-01** Security policy | 1.25 | HIPAA compliance requirement | **1.8x** | **2.25** |
| **PR.AC-07** Physical security | 1.25 | On-prem servers, medical devices | **1.5x** | **1.88** |
| **RS.MA-01** Incident response | 1.50 | HIPAA breach notification rules | **1.8x** | **2.70** |
| **ID.RA-01** Vulnerability management | 1.50 | Limited external exposure | **1.0x** | **1.50** |
| **DE.CM-01** Network monitoring | 1.25 | Internal network primary concern | **1.2x** | **1.50** |

**Top 3 Adjusted Gaps:**
1. RS.MA-01 (2.70) - IR plan required for HIPAA breach response
2. GV.PO-01 (2.25) - Security policy is HIPAA prerequisite
3. PR.DS-01 (2.00) - PHI encryption is regulatory mandate

---

#### Example 3: E-Commerce Startup

**Client Profile:**
- Online retail marketplace
- Processes payments (uses Stripe, no card data stored)
- Cloud-native (AWS, Shopify)
- PCI-DSS relevant but offloaded to payment processor
- 25 employees, rapid growth phase

**Context Adjustments:**

| Gap | Base Score | Reasoning | Multiplier | Adjusted Score |
|-----|------------|-----------|------------|----------------|
| **ID.RA-01** Vulnerability management | 1.50 | Public e-commerce site = target | **1.5x** | **2.25** |
| **PR.DS-02** Data-in-transit encryption | 1.20 | Customer payment flow protection | **1.5x** | **1.80** |
| **DE.CM-01** Network monitoring | 1.25 | Fraud detection needs | **1.4x** | **1.75** |
| **GV.SC-01** Supply chain risk | 1.25 | Heavy reliance on SaaS vendors | **1.3x** | **1.63** |
| **PR.AC-07** Physical security | 1.25 | Cloud-only, no physical assets | **0.5x** | **0.63** |
| **ID.AM-05** Asset criticality | 1.50 | Standard importance | **1.0x** | **1.50** |

**Top 3 Adjusted Gaps:**
1. ID.RA-01 (2.25) - Public site vulnerability = revenue impact
2. PR.DS-02 (1.80) - Customer payment data in transit
3. DE.CM-01 (1.75) - Fraud and abuse detection

---

### Documenting Context Decisions

For each adjusted gap in the Top 10, document the context rationale:

**Template:**

> **Gap:** [Control ID] [Control Name]  
> **Base Score:** [Framework weight × gap severity]  
> **Context:** [Brief client situation]  
> **Multiplier:** [1.5x] ([reason])  
> **Adjusted Score:** [Final priority]  
> **Risk if Unaddressed:** [Client-specific consequence]

**Example:**

> **Gap:** ID.RA-01 Vulnerabilities are identified and recorded  
> **Base Score:** 1.50  
> **Context:** B2B SaaS with public-facing application  
> **Multiplier:** 1.5x (High attack surface)  
> **Adjusted Score:** 2.25  
> **Risk if Unaddressed:** Exploitable known vulnerabilities in customer-facing platform = data breach affecting multiple clients, loss of trust, contract cancellations

---

### Top 10 Selection Process

After context adjustment:

1. **Calculate adjusted scores for all gaps** (Partial and No responses)
2. **Sort by adjusted_gap_score** (descending)
3. **Select Top 10** (or Top 15 if multiple ties at position 10)
4. **Document context rationale** for each
5. **Validate with assessor judgment**: Do these make sense for this client?

**Critical Rule:** Never show base framework scores to clients. Always present context-adjusted scores.

### Quality Control for Context Adjustment

Before finalizing prioritization:

- [ ] Threat context gathered (5 questions answered)
- [ ] Context multipliers applied to all gaps
- [ ] Top 10 gaps have different adjusted scores (not all identical)
- [ ] Risk rationale is client-specific (mentions their data, industry, or threat)
- [ ] Physical/irrelevant controls de-prioritized appropriately
- [ ] Compliance-blocking gaps elevated if timeline pressure exists

### Integration with Assessment Reports

**In Executive Summary:**

> **Scoring Methodology:**
> 
> Gap priorities were adjusted based on [Client]'s specific risk profile:
> - Data sensitivity: [PII / Payment / Health / etc.]
> - Infrastructure: [Cloud-only / Hybrid / On-premise]
> - Compliance: [SOC 2 / HIPAA / None]
> - Threat profile: [SaaS attack surface / etc.]
> 
> Priorities reflect [Client]'s actual risk, not generic framework weights.

**In Top 10 Table:**

Include "Context" column showing multiplier and brief reason:

| Rank | Control | Base | Context | Adjusted | Risk Rationale |
|------|---------|------|---------|----------|----------------|
| 1 | ID.RA-01 | 1.50 | 1.5x (SaaS) | 2.25 | Public services = breach risk |

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

CSFLite does not calculate risk scores, estimate breach probabilities, or model financial impact. These activities require a baseline of existing controls—exactly what CSFLite helps establish.

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
| Version | 1.0 |
| Last Updated | 2025-02-09 |
| Status | Active |
| Authoritative | Yes |

This document governs all CSFLite assessment methodology decisions. Conflicts between this document and other CSFLite documentation should be resolved in favor of this document.
