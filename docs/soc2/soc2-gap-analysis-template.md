# SOC 2 Readiness Gap Analysis

**Organization:** [Client Name]
**Assessment Date:** [Date]
**Assessor:** [Name / Firm]
**CSFLite Version:** 1.0.0
**SOC 2 Categories in Scope:** Security (CC1–CC9), Availability (A1), Confidentiality (C1)

> **Readiness Assessment Notice**
> This document is a readiness gap analysis prepared to help the organization identify areas of
> coverage and areas requiring remediation prior to a formal SOC 2 examination. It does not
> constitute SOC 2 compliance, a SOC 2 report, or any form of certification or audit opinion.
> Coverage determinations are based on evidence provided at the time of assessment and reflect
> whether controls exist, not whether they have been operating effectively over a sustained period.

---

## How to Use This Template

1. Complete the CSFLite governance assessment using `templates/governance_checks_template.csv`.
2. Complete the SOC 2 supplement questionnaire using `templates/soc2-supplement-questionnaire.csv`
   for any SOC 2 criterion areas not covered by the CSFLite 25 controls.
3. For each row in the tables below, enter the **Current State** (what evidence was reviewed) and
   **Evidence Assessed** (documents, screenshots, configurations observed).
4. Coverage status is pre-populated from the crosswalk (`docs/soc2/csflite-soc2-crosswalk.md`).
   Update if evidence reviewed changes the initial crosswalk rating.
5. Remediation recommendations are pre-populated as starting points. Adjust to reflect the
   organization's specific context and prioritization.

**Coverage status definitions:**
- `coverage exists` — controls are in place and evidence was reviewed
- `coverage partial` — controls partially address the criterion; gaps identified
- `coverage missing` — no controls or evidence found for this criterion area

---

## Security (CC1–CC9)

### CC1 — Control Environment

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC1.1 — Demonstrates commitment to integrity and ethical values | GV.PO-01 | coverage exists | | | |
| CC1.1 — Demonstrates commitment to integrity and ethical values | GV.RR-01 | coverage exists | | | |
| CC1.2 — Exercises oversight responsibility | GV.RR-01 | coverage exists | | | |
| CC1.2 — Exercises oversight responsibility | GV.RM-01 | coverage exists | | | |
| CC1.3 — Establishes structure, authority, and responsibility | GV.RR-01 | coverage exists | | | |
| CC1.3 — Establishes structure, authority, and responsibility | GV.PO-01 | coverage partial | | | Supplement policy with an explicit authority matrix or RACI that documents control activity ownership. |
| CC1.4 — Demonstrates commitment to competence | GV.OC-04 | coverage missing | | | Complete supplement questionnaire — Security Awareness (CC2) section. Document role-specific training requirements and completion records for security-sensitive roles. |
| CC1.5 — Enforces accountability | GV.RR-01 | coverage exists | | | |
| CC1.5 — Enforces accountability | GV.PO-01 | coverage partial | | | Document disciplinary procedures for policy violations and evidence of their application. |

### CC2 — Communication and Information

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC2.1 — Uses relevant information | DE.AE-02 | coverage partial | | | Document how security event analysis findings are escalated into management decision-making. |
| CC2.1 — Uses relevant information | ID.RA-05 | coverage partial | | | Confirm risk register is actively reviewed by leadership and used to inform control decisions. |
| CC2.2 — Communicates internally | GV.OC-01 | coverage missing | | | Complete supplement questionnaire — Security Awareness (CC2) section. Implement annual all-staff security awareness training with documented completion records. |
| CC2.2 — Communicates internally | PR.AT-01 | coverage missing | | | Complete supplement questionnaire — Security Awareness (CC2) section. Document communication of acceptable use policies and staff acknowledgment. |
| CC2.3 — Communicates externally | GV.SC-01 | coverage partial | | | Document processes for notifying customers or regulators of security events beyond incident notification. |
| CC2.3 — Communicates externally | RS.CO-02 | coverage partial | | | Expand incident communication plan to include proactive disclosure obligations (contractual, regulatory). |

### CC3 — Risk Assessment

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC3.1 — Specifies suitable objectives | GV.RM-01 | coverage exists | | | |
| CC3.2 — Identifies and analyzes risk | ID.RA-01 | coverage exists | | | |
| CC3.2 — Identifies and analyzes risk | ID.RA-05 | coverage exists | | | |
| CC3.3 — Assesses fraud risk | GV.RM-01 | coverage partial | | | Document explicit fraud risk scenarios in the risk register, including insider threat. |
| CC3.3 — Assesses fraud risk | ID.RA-05 | coverage partial | | | Confirm fraud and insider threat vectors are included in risk scoring methodology. |
| CC3.4 — Identifies significant change | ID.RA-01 | coverage partial | | | Complete supplement questionnaire — Change Management (CC8) section. Implement formal change management controls. |
| CC3.4 — Identifies significant change | GV.RM-01 | coverage partial | | | Document process for re-evaluating risk objectives when significant organizational or technology changes occur. |

### CC4 — Monitoring Activities

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC4.1 — Conducts ongoing or separate evaluations | DE.CM-01 | coverage exists | | | |
| CC4.1 — Conducts ongoing or separate evaluations | DE.CM-09 | coverage exists | | | |
| CC4.1 — Conducts ongoing or separate evaluations | DE.AE-02 | coverage exists | | | |
| CC4.2 — Evaluates and communicates deficiencies | DE.AE-08 | coverage exists | | | |
| CC4.2 — Evaluates and communicates deficiencies | RS.CO-02 | coverage exists | | | |

### CC5 — Control Activities

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC5.1 — Selects and develops control activities | GV.PO-01 | coverage exists | | | |
| CC5.1 — Selects and develops control activities | PR.AA-01 | coverage exists | | | |
| CC5.1 — Selects and develops control activities | PR.IR-01 | coverage exists | | | |
| CC5.2 — Selects and develops general technology controls | PR.DS-01 | coverage exists | | | |
| CC5.2 — Selects and develops general technology controls | PR.DS-02 | coverage exists | | | |
| CC5.2 — Selects and develops general technology controls | DE.CM-01 | coverage exists | | | |
| CC5.3 — Deploys through policies and procedures | GV.PO-01 | coverage exists | | | |
| CC5.3 — Deploys through policies and procedures | PR.AA-03 | coverage exists | | | |

### CC6 — Logical and Physical Access Controls

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC6.1 — Logical access security | PR.AA-01 | coverage exists | | | |
| CC6.1 — Logical access security | PR.AA-03 | coverage exists | | | |
| CC6.1 — Logical access security | PR.IR-01 | coverage exists | | | |
| CC6.2 — Prior to issuing credentials | PR.AA-01 | coverage exists | | | |
| CC6.3 — Role-based access controls | PR.AA-01 | coverage partial | | | Document RBAC implementation with role definitions, access matrices, and evidence of periodic access reviews. |
| CC6.4 — Restricts physical access | PR.AA-05 | coverage missing | | | Complete supplement questionnaire — Physical Access Controls (CC6.4) section. Implement and document physical access policy and controls for facilities housing critical systems. |
| CC6.4 — Restricts physical access | PR.AA-06 | coverage missing | | | Complete supplement questionnaire — Physical Access Controls (CC6.4) section. Deploy physical access logging and establish a log review cadence. |
| CC6.5 — Discontinues logical and physical access | PR.AA-01 | coverage partial | | | Document offboarding procedures for both logical (account deprovisioning) and physical (badge/key return) access removal with evidence of timely execution. |
| CC6.6 — External access | PR.AA-03 | coverage exists | | | |
| CC6.6 — External access | PR.IR-01 | coverage exists | | | |
| CC6.7 — Restricts transmission of information | PR.DS-02 | coverage exists | | | |
| CC6.8 — Prevents unauthorized software | DE.CM-09 | coverage exists | | | |

### CC7 — System Operations

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC7.1 — Detects new vulnerabilities | ID.RA-01 | coverage exists | | | |
| CC7.1 — Detects new vulnerabilities | DE.CM-09 | coverage exists | | | |
| CC7.2 — Monitors for anomalous behavior | DE.CM-01 | coverage exists | | | |
| CC7.2 — Monitors for anomalous behavior | DE.CM-09 | coverage exists | | | |
| CC7.3 — Evaluates security events | DE.AE-02 | coverage exists | | | |
| CC7.3 — Evaluates security events | DE.AE-08 | coverage exists | | | |
| CC7.4 — Responds to incidents | RS.MA-01 | coverage exists | | | |
| CC7.4 — Responds to incidents | RS.MI-01 | coverage exists | | | |
| CC7.4 — Responds to incidents | RS.MI-02 | coverage exists | | | |
| CC7.5 — Recovers from incidents | RC.RP-01 | coverage exists | | | |
| CC7.5 — Recovers from incidents | RC.CO-03 | coverage exists | | | |

### CC8 — Change Management

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC8.1 — Authorizes and implements changes | PR.PS-01 | coverage missing | | | Complete supplement questionnaire — Change Management (CC8) section. Establish a documented configuration management policy with approved baselines and a change approval workflow. |
| CC8.1 — Authorizes and implements changes | PR.PS-02 | coverage missing | | | Complete supplement questionnaire — Change Management (CC8) section. Implement a patch management process with risk-tiered patching timelines and EOL tracking. |
| CC8.1 — Authorizes and implements changes | PR.PS-04 | coverage missing | | | Complete supplement questionnaire — Change Management (CC8) section. Enable audit logging for privileged actions and configuration changes with defined retention periods. |
| CC8.1 — Authorizes and implements changes | PR.PS-06 | coverage missing | | | Complete supplement questionnaire — Change Management (CC8) section. Document SDLC procedures and production deployment approval gates. |
| CC8.1 — Authorizes and implements changes | ID.AM-02 | coverage partial | | | Use software inventory as the basis for a change register; formalize tracking of approved vs. unauthorized changes. |

### CC9 — Risk Mitigation

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| CC9.1 — Identifies and develops risk mitigation | ID.RA-05 | coverage exists | | | |
| CC9.1 — Identifies and develops risk mitigation | GV.RM-01 | coverage exists | | | |
| CC9.2 — Assesses vendor and partner risk | GV.SC-01 | coverage exists | | | |
| CC9.2 — Assesses vendor and partner risk | ID.RA-01 | coverage partial | | | Confirm vulnerability tracking scope includes vendor-managed components and third-party systems with access to your environment. |

---

## Availability (A1)

### A1 — Availability Criteria

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| A1.1 — Maintains environmental protections and alternative processing | PR.DS-11 | coverage partial | | | Complete supplement questionnaire — Business Continuity (A1) section. Document environmental controls (power, cooling) and alternative processing arrangements. |
| A1.1 — Maintains environmental protections and alternative processing | RC.RP-02 | coverage missing | | | Complete supplement questionnaire — Business Continuity (A1) section. Develop a BCP identifying critical systems, recovery priorities, and alternative processing site or cloud failover arrangements. |
| A1.2 — Maintains backup and recovery consistent with objectives | PR.DS-11 | coverage exists | | | |
| A1.2 — Maintains backup and recovery consistent with objectives | RC.RP-01 | coverage exists | | | |
| A1.2 — Maintains backup and recovery consistent with objectives | RC.RP-03 | coverage missing | | | Complete supplement questionnaire — Business Continuity (A1) section. Document pre-restoration backup integrity verification steps and implement as part of the standard restoration procedure. |
| A1.3 — Tests recovery plan objectives | RC.RP-01 | coverage exists | | | |
| A1.3 — Tests recovery plan objectives | RC.RP-04 | coverage missing | | | Complete supplement questionnaire — Business Continuity (A1) section. Document critical function dependencies within the BCP and confirm cybersecurity controls are included in recovery scope. |
| A1.3 — Tests recovery plan objectives | RC.RP-05 | coverage missing | | | Complete supplement questionnaire — Business Continuity (A1) section. Implement a post-incident continuity evaluation process and feed findings back into the BCP. |

---

## Confidentiality (C1)

### C1 — Confidentiality Criteria

| SOC 2 Criterion | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|
| C1.1 — Identifies and maintains confidential information | PR.DS-01 | coverage exists | | | |
| C1.1 — Identifies and maintains confidential information | PR.DS-02 | coverage exists | | | |
| C1.1 — Identifies and maintains confidential information | ID.AM-05 | coverage exists | | | |
| C1.2 — Disposes of confidential information | PR.DS-03 | coverage missing | | | Complete supplement questionnaire — Data Disposal (C1.2) section. Develop and document a data and media disposal policy referencing approved sanitization methods (e.g. NIST SP 800-88). |
| C1.2 — Disposes of confidential information | PR.DS-10 | coverage missing | | | Complete supplement questionnaire — Data Disposal (C1.2) section. Implement hardware sanitization verification procedures and maintain disposal records (chain-of-custody, certificates of destruction). |

---

## Coverage Summary

| SOC 2 Category | Coverage Exists | Coverage Partial | Coverage Missing |
|---|---|---|---|
| CC1 — Control Environment | | | |
| CC2 — Communication and Information | | | |
| CC3 — Risk Assessment | | | |
| CC4 — Monitoring Activities | | | |
| CC5 — Control Activities | | | |
| CC6 — Logical and Physical Access | | | |
| CC7 — System Operations | | | |
| CC8 — Change Management | | | |
| CC9 — Risk Mitigation | | | |
| A1 — Availability | | | |
| C1 — Confidentiality | | | |
| **Total** | | | |

*Assessor populates counts after reviewing all findings above.*

---

## Priority Remediation Items

Rank items by SOC 2 impact (mandatory criteria first, then breadth of gap, then remediation effort).

| Priority | SOC 2 Criterion | Gap Description | Recommended Action | Effort Estimate |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

## Assessor Sign-Off

| | |
|---|---|
| Prepared by | |
| Review date | |
| Next assessment recommended | |

*This readiness gap analysis does not constitute a SOC 2 report, audit opinion, or certification of compliance.*
