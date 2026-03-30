# HIPAA Readiness Gap Analysis

**Organization:** [Client Name]
**Assessment Date:** [Date]
**Assessor:** [Name / Firm]
**CSFLite Version:** 1.0.0
**Client Type:** Business Associate (BA)
**HIPAA Scope:** Security Rule (45 CFR §164.308, §164.310, §164.312), Organizational Requirements — BAA provisions (§164.314(a)(2)(i)), Breach Notification Rule — BA obligations (§164.400–414)

> **Readiness Assessment Notice**
> This document is a HIPAA readiness gap analysis prepared to help the organization identify areas
> of coverage and areas requiring remediation prior to handling electronic Protected Health Information
> (ePHI) for US healthcare Covered Entities. It does not constitute HIPAA compliance, a HIPAA audit,
> or certification of any kind. Coverage determinations reflect whether controls exist at the time of
> assessment, not whether they have been operating effectively over a sustained period. This engagement
> identifies the client as a **Business Associate** and frames all findings in the context of BA
> obligations under 45 CFR Part 164. It does not constitute a legal opinion on BAA sufficiency or
> any other legal matter.

---

## How to Use This Template

1. Complete the CSFLite governance assessment using `templates/governance_checks_template.csv`.
2. Complete the HIPAA supplement questionnaire using `templates/hipaa-supplement-questionnaire.csv`
   for HIPAA requirements not covered by the CSFLite 25 controls (Q1–Q9).
3. For each row below, enter **Current State** (what controls or practices were observed) and
   **Evidence Assessed** (documents, configurations, or records reviewed).
4. Coverage status is pre-populated from the crosswalk (`docs/hipaa/csflite-hipaa-crosswalk.md`).
   Update if evidence reviewed changes the initial crosswalk rating.
5. Remediation recommendations are pre-populated as starting points. Adjust for the client's
   specific context, workforce model (on-site, remote, or hybrid), and risk tolerance.

**Coverage status definitions:**
- `coverage exists` — controls are in place and evidence was reviewed
- `coverage partial` — controls partially address the requirement; ePHI-scoping gaps or missing documentation identified
- `coverage missing` — no controls or insufficient evidence found for this requirement area

---

## Administrative Safeguards — §164.308

### §164.308(a)(1) Security Management Process

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(1)(i) | Risk Analysis | R | ID.RA-01, ID.RA-05, GV.RM-01 | coverage exists | | | Confirm ePHI systems are explicitly included in vulnerability scan scope and risk register. |
| §164.308(a)(1)(ii) | Risk Management | R | GV.RM-01, GV.PO-01 | coverage exists | | | |
| §164.308(a)(1)(iii) | Sanction Policy | R | GV.PO-01 | coverage partial | | | Add an explicit HIPAA sanction policy section to the cybersecurity policy or issue a standalone sanction policy specifying consequences for security policy violations by workforce members with ePHI access. |
| §164.308(a)(1)(iv) | Information System Activity Review | R | DE.CM-01, DE.CM-09, DE.AE-02 | coverage partial | | | Document that activity review procedures explicitly include ePHI-touching systems; confirm review logs are retained for the minimum required period. |

### §164.308(a)(2) Assigned Security Responsibility

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(2) | Assigned Security Responsibility | R | GV.RR-01 | coverage exists | | | |

### §164.308(a)(3) Workforce Security

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(3)(i) | Authorization and/or Supervision | A | GV.RR-01 | coverage partial | | | Document supervisory procedures for workforce members with ePHI access. Complete Supplement Q8. |
| §164.308(a)(3)(ii) | Workforce Clearance Procedure | A | GV.RR-04 | coverage missing | | | Implement pre-access clearance procedures for workforce members whose roles involve ePHI access. Complete Supplement Q8. |
| §164.308(a)(3)(iii) | Termination Procedures | A | PR.AA-05 | coverage missing | | | Document and operationalize ePHI access revocation procedures for termination, role change, and disciplinary action. Complete Supplement Q8. |

### §164.308(a)(4) Information Access Management

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(4)(i) | Isolating Healthcare Clearinghouse Function | R | PR.IR-01 | coverage exists | | | Note: this specification is N/A for organizations that do not operate a healthcare clearinghouse. Document as N/A if not applicable. |
| §164.308(a)(4)(ii) | Access Authorization | A | PR.AA-01 | coverage exists | | | |
| §164.308(a)(4)(iii) | Access Establishment and Modification | A | PR.AA-01, PR.AA-03 | coverage exists | | | |

### §164.308(a)(5) Security Awareness and Training

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(5)(i) | Security Reminders | A | PR.AT-01 | coverage missing | | | Implement periodic HIPAA-specific security reminders for all workforce members with ePHI access. Complete Supplement Q4. |
| §164.308(a)(5)(ii) | Protection from Malicious Software | A | DE.CM-09 | coverage partial | | | Confirm endpoint protection covers all ePHI-touching systems; document malware detection, guarding, and reporting procedures. |
| §164.308(a)(5)(iii) | Log-in Monitoring | A | DE.CM-01, DE.AE-02 | coverage partial | | | Verify ePHI systems are within monitoring scope and that login anomaly detection procedures for ePHI systems are documented. |
| §164.308(a)(5)(iv) | Password Management | A | PR.AA-01 | coverage exists | | | |

### §164.308(a)(6) Security Incident Procedures

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(6) | Response and Reporting | R | RS.MA-01, RS.MI-01, RS.MI-02, RS.CO-02, DE.AE-08 | coverage exists | | | Confirm IR plan explicitly covers ePHI-involving incidents and includes escalation to Covered Entity clients per §164.410. |

### §164.308(a)(7) Contingency Plan

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(7)(i) | Data Backup Plan | R | PR.DS-11 | coverage exists | | | Confirm backup scope includes all ePHI data stores and that backup copies are retrievable within the defined RTO. |
| §164.308(a)(7)(ii) | Disaster Recovery Plan | R | RC.RP-01 | coverage partial | | | Document a formal DR plan identifying ePHI system priorities and defined RTO/RPO. Complete Supplement Q7. |
| §164.308(a)(7)(iii) | Emergency Mode Operation Plan | R | RS.MA-01 | coverage partial | | | Add an emergency mode operation section to the IR plan documenting how ePHI access is maintained during system failures. Complete Supplement Q7. |
| §164.308(a)(7)(iv) | Testing and Revision Procedures | A | PR.DS-11, RC.RP-01 | coverage partial | | | Document contingency plan test results (not only backup restoration) and maintain a revision log updated after each test. Complete Supplement Q7. |
| §164.308(a)(7)(v) | Applications and Data Criticality Analysis | A | ID.AM-05 | coverage exists | | | Confirm criticality analysis explicitly identifies ePHI-processing applications and their recovery priority. |

### §164.308(a)(8) Periodic Evaluation

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(a)(8) | Periodic Evaluation | R | GV.RM-01 | advisory | This engagement satisfies the §164.308(a)(8) evaluation requirement. | N/A — advisory | Establish a recurring evaluation schedule. Annual assessment is recommended. Record evaluation date and schedule the next assessment. |

### §164.308(b)(1) Business Associate Contracts

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.308(b)(1) | Business Associate Contracts | R | GV.SC-01 | coverage partial | | | Verify executed BAAs exist with all CE clients and with subcontractors who access ePHI. Complete Supplement Q5. BAA content sufficiency review is out of scope. |

---

## Physical Safeguards — §164.310

### §164.310(a)(1) Facility Access Controls

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.310(a)(1)(i) | Contingency Operations | A | RC.RP-01 | coverage partial | | | Add physical access contingency procedures to the BCP documenting how workforce accesses ePHI facilities during a disaster or emergency. Complete Supplement Q7. |
| §164.310(a)(1)(ii) | Facility Security Plan | A | PR.AA-06 | coverage missing | | | Develop a facility security plan documenting physical access controls, security measures, and access authorization procedures for all locations housing ePHI systems. Complete Supplement Q2. |
| §164.310(a)(1)(iii) | Access Control and Validation Procedures | A | PR.AA-06 | coverage missing | | | Implement and document physical access validation procedures (badge readers, visitor sign-in, escort policies) for ePHI facilities. Complete Supplement Q2. |
| §164.310(a)(1)(iv) | Maintenance Records | A | — | coverage missing | | | Implement a maintenance log for physical components of ePHI facilities (locks, badge readers, security hardware). No CSF equivalent — HIPAA-specific recordkeeping requirement. Complete Supplement Q2. |

### §164.310(b) Workstation Use

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.310(b) | Workstation Use | R | PR.AA-06 | coverage missing | | | Develop and deploy a workstation use policy specifying proper functions, physical surroundings, and acceptable use for workstations that access ePHI. For remote/hybrid workforce, include home environment physical security requirements (screen positioning, privacy screens, locked storage). Complete Supplement Q2. |

### §164.310(c) Workstation Security

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.310(c) | Workstation Security | R | PR.AA-06 | coverage missing | | | Implement physical security measures for all workstations accessing ePHI (screen locks enforced by policy, cable locks for portable devices, secure physical positioning). For remote/hybrid workforce, enforce via workstation use policy and screen lock configuration management. Complete Supplement Q2. |

### §164.310(d) Device and Media Controls

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.310(d)(1)(i) | Disposal | R | PR.DS-03 | coverage missing | | | Develop a media disposal policy specifying approved sanitization methods (reference NIST SP 800-88) for ePHI-containing hardware and electronic media. Implement and log all disposal activities with certificates of destruction. Complete Supplement Q3. |
| §164.310(d)(1)(ii) | Media Re-use | R | PR.DS-03 | coverage missing | | | Document and implement procedures for sanitizing electronic media before re-use to ensure all ePHI is removed and unrecoverable. Maintain re-use records. Complete Supplement Q3. |
| §164.310(d)(1)(iii) | Accountability | A | ID.AM-01 | coverage partial | | | Extend hardware inventory to track movements and activities of hardware and electronic media containing ePHI. Complete Supplement Q3. |
| §164.310(d)(1)(iv) | Data Backup and Storage | A | PR.DS-11 | coverage exists | | | |

---

## Technical Safeguards — §164.312

### §164.312(a)(1) Access Control

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.312(a)(1)(i) | Unique User Identification | R | PR.AA-01, PR.AA-03 | coverage exists | | | |
| §164.312(a)(1)(ii) | Emergency Access Procedure | R | RS.MA-01 | coverage partial | | | Add a documented emergency access procedure to the IR plan specifying how authorized personnel obtain ePHI access during system failures when normal access controls cannot be followed. Coverage note: ePHI-specific aspect; not a separate gap. |
| §164.312(a)(1)(iii) | Automatic Logoff | A | PR.AA-03 | coverage partial | | | Confirm and document that automatic session timeout is configured and enforced on all ePHI-touching systems. Coverage note: ePHI-specific scoping confirmation required. |
| §164.312(a)(1)(iv) | Encryption and Decryption | A | PR.DS-01, PR.DS-02 | coverage exists | | | Confirm encryption is applied to all ePHI data stores and all transmission paths, not only the network perimeter. |

### §164.312(b) Audit Controls

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.312(b) | Audit Controls | R | DE.CM-01, DE.CM-09, DE.AE-02 | coverage partial | | | Verify audit logs capture activity on all ePHI-touching systems, that logs are protected from unauthorized modification, and that log retention period is documented. Coverage note: ePHI-specific audit logging; not a separate gap. |

### §164.312(c)(1) Integrity

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.312(c)(1) | Mechanism to Authenticate ePHI Integrity | A | PR.DS-01, PR.DS-02 | coverage exists | | | Confirm integrity mechanisms (checksums, authenticated encryption, HMAC) are applied to ePHI both at rest and in transit. |

### §164.312(d) Person or Entity Authentication

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.312(d) | Person or Entity Authentication | R | PR.AA-01, PR.AA-03 | coverage exists | | | |

### §164.312(e)(1) Transmission Security

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.312(e)(1)(i) | Integrity Controls | A | PR.DS-02 | coverage exists | | | |
| §164.312(e)(1)(ii) | Encryption | A | PR.DS-02, PR.IR-01 | coverage exists | | | Confirm TLS 1.2+ is enforced for all ePHI transmission paths including internal network segments carrying ePHI. |

---

## Organizational Requirements — §164.314

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.314(a)(2)(i) | Business Associate Subcontractor Agreements | R | GV.SC-01 | coverage partial | | | Verify that all subcontractors and vendors who access ePHI have executed BAAs. Complete Supplement Q5. |

---

## Breach Notification Rule — §164.400–414

| HIPAA Section | Standard / Impl. Spec. | Req/Addr | Mapped CSF Subcategory | CSFLite Coverage | Current State | Evidence Assessed | Remediation Recommendation |
|---|---|---|---|---|---|---|---|
| §164.410 | Notification by Business Associates | R | RS.CO-02, DE.AE-08 | coverage partial | | | Develop or update breach notification procedures to include: discovery-to-notification timeline tracking (60-day maximum), required §164.410(c) notification content elements, and designated CE notification contacts. Complete Supplement Q6. |
| §164.412 | Law Enforcement Delay | R | RS.CO-02 | coverage partial | | | Add a law enforcement delay hold process to the breach notification procedure documenting how the BA responds to a law enforcement request to delay CE notification per §164.412. Complete Supplement Q6. |

---

## Coverage Summary

| HIPAA Safeguard Category | Coverage Exists | Coverage Partial | Coverage Missing | Advisory |
|---|---|---|---|---|
| Administrative Safeguards (§164.308) | | | | |
| Physical Safeguards (§164.310) | | | | |
| Technical Safeguards (§164.312) | | | | |
| Organizational Requirements (§164.314) | | | | |
| Breach Notification Rule (§164.400–414) | | | | |
| **Total** | | | | |

*Assessor populates counts after reviewing all findings above.*

---

## Priority Remediation Items

Rank by HIPAA impact: Required specifications with `coverage missing` status first, then Required with `coverage partial`, then Addressable gaps, then ePHI coverage note items.

| Priority | HIPAA Section | Gap Description | Recommended Action | Effort Estimate |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

## Advisory Notes

**§164.308(a)(8) — Periodic Evaluation:** This engagement satisfies the §164.308(a)(8) periodic evaluation requirement. The client should establish a recurring evaluation schedule — annually is recommended. Record the evaluation date and schedule the next assessment.

**§164.316(b)(2) — Documentation Retention:** All policies, procedures, and records produced or reviewed during this engagement must be retained for a minimum of 6 years from creation or last effective date (45 CFR §164.316(b)(2)(i)). This is an administrative constraint, not an assessed gap.

---

## Assessor Sign-Off

| | |
|---|---|
| Prepared by | |
| Review date | |
| Next assessment recommended | |

*This readiness gap analysis does not constitute a HIPAA audit, HIPAA compliance certification, or a legal opinion. Prepared using CSFLite v1.0.0 — [csflite-hipaa-crosswalk.md](csflite-hipaa-crosswalk.md)*
