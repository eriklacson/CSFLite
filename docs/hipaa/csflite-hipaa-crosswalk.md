# CSFLite to HIPAA Security Rule Crosswalk

**Framework:** NIST CSF 2.0 (CSWP 29) → HIPAA Security Rule (45 CFR Part 164 Subpart C) and Breach Notification Rule (45 CFR Part 164 Subpart D)
**CSFLite version:** 1.0.0 (25 controls — see `csflite/controls.json`)
**Architectural basis:** [ADR-0001](../adr/ADR-0001-full-csf-crosswalk.md)
**Scope:** Administrative Safeguards (§164.308), Physical Safeguards (§164.310), Technical Safeguards (§164.312), Organizational Requirements — BA subcontractor provisions (§164.314(a)(2)(i)), Breach Notification Rule — BA obligations (§164.400–414)
**Excluded:** Privacy Rule (§164.500 series); Documentation Requirements (§164.316) and Periodic Evaluation (§164.308(a)(8)) are advisory notes, not assessed gaps; Clearinghouse isolation (§164.308(a)(4)(i)) is noted as inapplicable to most BAs
**Client context:** Business Associate obligations for Philippine SMBs (20–200 employees) serving US healthcare Covered Entities

**Coverage ratings:**
- `full` — CSF subcategory is in the CSFLite 25 and directly evidences the HIPAA standard or implementation specification
- `partial` — CSF subcategory is in the CSFLite 25 but only partially evidences the requirement, or requires ePHI-scoping confirmation; expressed as `coverage partial` in the gap analysis
- `gap` — requirement maps to a CSF subcategory outside the CSFLite 25; addressed by `templates/hipaa-supplement-questionnaire.csv`; expressed as `coverage missing` in the gap analysis
- `advisory` — requirement is a constraint or advisory note; not assessed as a gap

**Required vs. Addressable:** HIPAA Security Rule implementation specifications are designated Required (R) or Addressable (A). Addressable specifications must be implemented if reasonable and appropriate, or the BA must document an equivalent alternative measure and the rationale for non-implementation.

---

## Administrative Safeguards — §164.308

### §164.308(a)(1) Security Management Process

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(1)(i) | Risk Analysis | R | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Yes | full | Regular vulnerability scanning and a maintained vulnerability register directly evidence risk analysis. ePHI systems should be explicitly included in scan scope and risk register. |
| §164.308(a)(1)(i) | Risk Analysis | R | ID.RA-05 | Threats and vulnerabilities are used to understand inherent risk and prioritize response | Yes | full | Risk scoring methodology using likelihood × impact directly evidences formal risk analysis with inherent risk assessment and prioritized response. |
| §164.308(a)(1)(i) | Risk Analysis | R | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | full | Stakeholder-agreed risk management objectives document the organizational risk management framework required by the Security Management Process standard. |
| §164.308(a)(1)(ii) | Risk Management | R | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | full | Documented risk management objectives with leadership agreement evidence implementation of risk management activities to reduce identified risks to a reasonable and appropriate level. |
| §164.308(a)(1)(ii) | Risk Management | R | GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context and priorities | Yes | full | Cybersecurity policy establishing risk management context and priorities evidences the organizational framework for ongoing risk management. |
| §164.308(a)(1)(iii) | Sanction Policy | R | GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context and priorities | Yes | partial | Cybersecurity policy covers organizational obligations; HIPAA requires an explicit sanction policy documenting consequences for workforce members who fail to comply with security policies. Supplement the governance policy with a dedicated sanction section or standalone document. |
| §164.308(a)(1)(iv) | Information System Activity Review | R | DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Yes | full | Network monitoring with documented alert rules and review procedures directly evidences regular review of information system activity. |
| §164.308(a)(1)(iv) | Information System Activity Review | R | DE.CM-09 | Computing hardware and software are monitored to find potentially adverse events | Yes | full | Endpoint monitoring covers hardware and software activity review for ePHI-touching systems. Confirm all ePHI systems are within monitoring scope. |
| §164.308(a)(1)(iv) | Information System Activity Review | R | DE.AE-02 | Potentially adverse events are analyzed to understand associated activities | Yes | partial | Alert triage and analysis procedures provide the review mechanism; HIPAA requires review logs for ePHI systems to be examined for anomalies. Verify ePHI system logs are within triage scope and that review is documented. |

### §164.308(a)(2) Assigned Security Responsibility

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(2) | Assigned Security Responsibility | R | GV.RR-01 | Organizational leadership is responsible and accountable for cybersecurity risk | Yes | full | A named individual or role with documented authority and accountability for cybersecurity risk directly evidences the requirement to designate a security official responsible for HIPAA Security Rule compliance. |

### §164.308(a)(3) Workforce Security

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(3)(i) | Authorization and/or Supervision | A | GV.RR-01 | Organizational leadership is responsible and accountable for cybersecurity risk | Yes | partial | Leadership accountability is documented; HIPAA additionally requires supervisory procedures for workforce members whose work involves ePHI access. See Supplement Q8 for workforce authorization evidence. |
| §164.308(a)(3)(ii) | Workforce Clearance Procedure | A | GV.RR-04 | Cybersecurity is included in human resources practices | No | gap | Pre-access clearance procedures for workforce members with ePHI access are outside CSFLite 25. See Supplement Q8. |
| §164.308(a)(3)(iii) | Termination Procedures | A | PR.AA-05 | Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed | No | gap | Procedures for revoking ePHI access upon termination or role change are outside CSFLite 25. See Supplement Q8. |

### §164.308(a)(4) Information Access Management

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(4)(i) | Isolating Healthcare Clearinghouse Function | R | PR.IR-01 | Networks and environments are protected from unauthorized logical access | Yes | full | Network segmentation and isolation controls address the clearinghouse isolation requirement. Note: this specification applies only to covered entities that operate healthcare clearinghouse functions; most BAs are not subject to this requirement and should document it as N/A. |
| §164.308(a)(4)(ii) | Access Authorization | A | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | Identity and credential management including provisioning processes directly evidence ePHI access authorization requirements. |
| §164.308(a)(4)(iii) | Access Establishment and Modification | A | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | Credential management processes covering provisioning and modification directly evidence this specification. |
| §164.308(a)(4)(iii) | Access Establishment and Modification | A | PR.AA-03 | Users and services are authenticated | Yes | full | Authentication controls enforce authorized access at all access establishment and modification points. |

### §164.308(a)(5) Security Awareness and Training

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(5)(i) | Security Reminders | A | PR.AT-01 | Awareness activities are provided | No | gap | Periodic security reminders for all workforce members with ePHI access are outside CSFLite 25. See Supplement Q4. |
| §164.308(a)(5)(ii) | Protection from Malicious Software | A | DE.CM-09 | Computing hardware and software are monitored to find potentially adverse events | Yes | partial | Endpoint monitoring detects malicious software; HIPAA additionally requires documented procedures for guarding against, detecting, and reporting malicious software. Confirm endpoint protection covers all ePHI-touching systems and that procedures are documented. |
| §164.308(a)(5)(iii) | Log-in Monitoring | A | DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Yes | partial | Network monitoring captures login events at the boundary; HIPAA requires monitoring login attempts to ePHI information systems specifically. Verify ePHI systems are within monitoring scope. |
| §164.308(a)(5)(iii) | Log-in Monitoring | A | DE.AE-02 | Potentially adverse events are analyzed to understand associated activities | Yes | partial | Alert analysis procedures address event review; login anomaly detection for ePHI systems should be explicitly included in triage SOPs. |
| §164.308(a)(5)(iv) | Password Management | A | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | Password policy, MFA enforcement, and credential management procedures directly evidence password management requirements. |

### §164.308(a)(6) Security Incident Procedures

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(6) | Response and Reporting | R | RS.MA-01 | The incident response plan is executed in coordination with relevant third parties | Yes | full | Tested IR plan with third-party coordination directly evidences the incident response requirement, including coordination with Covered Entity clients for ePHI-involving incidents. |
| §164.308(a)(6) | Response and Reporting | R | RS.MI-01 | Incidents are contained | Yes | full | Containment playbooks with isolation capability directly address incident containment procedures. |
| §164.308(a)(6) | Response and Reporting | R | RS.MI-02 | Incidents are eradicated | Yes | full | Eradication procedures and post-incident validation complete the response-to-recovery lifecycle. |
| §164.308(a)(6) | Response and Reporting | R | RS.CO-02 | Internal and external stakeholders are notified of incidents | Yes | full | Notification procedures and communication templates address incident reporting obligations, including escalation to Covered Entity clients for ePHI-involving incidents per §164.410. |
| §164.308(a)(6) | Response and Reporting | R | DE.AE-08 | Incidents are declared when adverse events meet defined incident criteria | Yes | full | Incident declaration criteria formalize the threshold for invoking HIPAA-required incident response procedures. |

### §164.308(a)(7) Contingency Plan

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(7)(i) | Data Backup Plan | R | PR.DS-11 | Backups of data are created and tested | Yes | full | Backup schedule with regular restoration testing and verification reports directly evidence the data backup plan requirement for ePHI. |
| §164.308(a)(7)(ii) | Disaster Recovery Plan | R | RC.RP-01 | The recovery portion of the incident response plan is executed | Yes | partial | Recovery plan execution covers disaster recovery procedures; a formal DR plan document addressing ePHI system priorities and defined RTO/RPO is assessed via Supplement Q7. |
| §164.308(a)(7)(iii) | Emergency Mode Operation Plan | R | RS.MA-01 | The incident response plan is executed in coordination with relevant third parties | Yes | partial | IR plan addresses emergency coordination; HIPAA additionally requires a documented plan for maintaining critical ePHI access and business operations during system failures. See Supplement Q7. |
| §164.308(a)(7)(iv) | Testing and Revision Procedures | A | PR.DS-11 | Backups of data are created and tested | Yes | partial | Backup restoration testing is documented; HIPAA also requires testing the contingency plan as a whole and updating it based on test results. See Supplement Q7. |
| §164.308(a)(7)(iv) | Testing and Revision Procedures | A | RC.RP-01 | The recovery portion of the incident response plan is executed | Yes | partial | Annual recovery testing is documented; broader contingency plan testing and revision procedures are assessed via Supplement Q7. |
| §164.308(a)(7)(v) | Applications and Data Criticality Analysis | A | ID.AM-05 | Assets are prioritized based on classification and criticality | Yes | full | Asset prioritization based on classification and criticality directly evidences the requirement to assess which applications and data are critical to business operations. |

### §164.308(a)(8) Periodic Evaluation

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(a)(8) | Periodic Evaluation | R | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | advisory | This engagement satisfies the §164.308(a)(8) periodic evaluation requirement. Advisory: the client should establish a recurring evaluation schedule — annually is recommended. Not assessed as a separate gap. |

### §164.308(b)(1) Business Associate Contracts

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.308(b)(1) | Business Associate Contracts and Other Arrangements | R | GV.SC-01 | A cybersecurity supply chain risk management program is established | Yes | partial | Supply chain risk management including vendor security requirements partially addresses BA obligations; BAA existence with Covered Entity clients and subcontractors is verified via Supplement Q5. Legal sufficiency review of BAA content is out of scope. |

---

## Physical Safeguards — §164.310

### §164.310(a)(1) Facility Access Controls

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.310(a)(1)(i) | Contingency Operations | A | RC.RP-01 | The recovery portion of the incident response plan is executed | Yes | partial | Recovery plan execution covers disaster recovery procedures; HIPAA additionally requires documented procedures for obtaining necessary ePHI during emergencies involving physical access disruptions. See Supplement Q7. |
| §164.310(a)(1)(ii) | Facility Security Plan | A | PR.AA-06 | Physical access to assets is managed, monitored, and enforced commensurate with risk | No | gap | A formal plan to safeguard facilities and equipment from unauthorized physical access, tampering, and theft is outside CSFLite 25. See Supplement Q2. |
| §164.310(a)(1)(iii) | Access Control and Validation Procedures | A | PR.AA-06 | Physical access to assets is managed, monitored, and enforced commensurate with risk | No | gap | Physical access control and validation procedures for ePHI facilities (badge readers, visitor escort policies) are outside CSFLite 25. See Supplement Q2. |
| §164.310(a)(1)(iv) | Maintenance Records | A | — | No CSF 2.0 equivalent | — | gap | Physical facility maintenance records have no direct NIST CSF 2.0 subcategory equivalent. Documented as HIPAA-specific recordkeeping requirement. See Supplement Q2. |

### §164.310(b) Workstation Use

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.310(b) | Workstation Use | R | PR.AA-06 | Physical access to assets is managed, monitored, and enforced commensurate with risk | No | gap | Policies specifying workstation function, physical surroundings, and manner of use for ePHI access are outside CSFLite 25. Remote/hybrid workforce qualifier applies — evidence shifts from physical access logs to workstation use policy enforcement and screen privacy controls. See Supplement Q2. |

### §164.310(c) Workstation Security

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.310(c) | Workstation Security | R | PR.AA-06 | Physical access to assets is managed, monitored, and enforced commensurate with risk | No | gap | Physical security measures for workstations accessing ePHI (screen locks, cable locks, secure positioning, privacy screens) are outside CSFLite 25. Remote/hybrid qualifier applies. See Supplement Q2. |

### §164.310(d) Device and Media Controls

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.310(d)(1)(i) | Disposal | R | PR.DS-03 | Assets are formally managed throughout removal, transfers, and disposition | No | gap | Policies and procedures for final disposal of ePHI from hardware and electronic media (including physical destruction or NIST SP 800-88 sanitization) are outside CSFLite 25. See Supplement Q3. |
| §164.310(d)(1)(ii) | Media Re-use | R | PR.DS-03 | Assets are formally managed throughout removal, transfers, and disposition | No | gap | Procedures for removing ePHI from electronic media before re-use are outside CSFLite 25. See Supplement Q3. |
| §164.310(d)(1)(iii) | Accountability | A | ID.AM-01 | Inventories of hardware managed by the organization are maintained | Yes | partial | Hardware asset inventory provides the foundation for media accountability; HIPAA additionally requires tracking movements and activities of hardware and electronic media containing ePHI. See Supplement Q3. |
| §164.310(d)(1)(iv) | Data Backup and Storage | A | PR.DS-11 | Backups of data are created and tested | Yes | full | Backup creation and restoration testing directly evidences the data backup and storage specification for ePHI. |

---

## Technical Safeguards — §164.312

### §164.312(a)(1) Access Control

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.312(a)(1)(i) | Unique User Identification | R | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | Credential management requiring unique user IDs for all users and services directly evidences this required specification. |
| §164.312(a)(1)(i) | Unique User Identification | R | PR.AA-03 | Users and services are authenticated | Yes | full | Authentication controls enforce unique user identification at all ePHI system access points. |
| §164.312(a)(1)(ii) | Emergency Access Procedure | R | RS.MA-01 | The incident response plan is executed in coordination with relevant third parties | Yes | partial | IR plan covers emergency coordination; HIPAA requires a specific documented procedure for obtaining necessary ePHI during emergencies when normal access controls cannot be followed. Coverage note: ePHI-specific aspect; not a separate gap. Verify IR plan includes emergency access procedures. |
| §164.312(a)(1)(iii) | Automatic Logoff | A | PR.AA-03 | Users and services are authenticated | Yes | partial | Authentication controls include session management; HIPAA requires automatic termination of electronic sessions for ePHI systems after a predetermined period of inactivity. Coverage note: verify session timeout is configured and enforced on all ePHI-touching systems. |
| §164.312(a)(1)(iv) | Encryption and Decryption | A | PR.DS-01 | The confidentiality and integrity of data-at-rest are protected | Yes | full | Encryption at rest for ePHI data stores directly evidences this addressable specification. |
| §164.312(a)(1)(iv) | Encryption and Decryption | A | PR.DS-02 | The confidentiality and integrity of data-in-transit are protected | Yes | full | TLS enforcement for ePHI in transit directly evidences this addressable specification. |

### §164.312(b) Audit Controls

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.312(b) | Audit Controls | R | DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Yes | partial | Network monitoring provides audit of network-level activity; HIPAA requires hardware, software, and procedural mechanisms to record and examine activity in information systems containing ePHI. Coverage note: verify audit logs capture ePHI system activity and are retained for the minimum required period. |
| §164.312(b) | Audit Controls | R | DE.CM-09 | Computing hardware and software are monitored to find potentially adverse events | Yes | partial | Endpoint monitoring covers system-level activity audit; confirm all ePHI-touching systems are within audit scope and that logs are protected from unauthorized modification. |
| §164.312(b) | Audit Controls | R | DE.AE-02 | Potentially adverse events are analyzed to understand associated activities | Yes | partial | Alert triage procedures provide the review mechanism; ePHI-specific activity review should be explicitly documented as part of alert triage SOPs. Coverage note: ePHI-specific audit logging is assessed as a coverage note, not a separate gap. |

### §164.312(c)(1) Integrity

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.312(c)(1) | Mechanism to Authenticate ePHI Integrity | A | PR.DS-01 | The confidentiality and integrity of data-at-rest are protected | Yes | full | Integrity controls for ePHI at rest (checksums, authenticated encryption) directly address this addressable specification. |
| §164.312(c)(1) | Mechanism to Authenticate ePHI Integrity | A | PR.DS-02 | The confidentiality and integrity of data-in-transit are protected | Yes | full | Integrity controls for ePHI in transit (TLS with integrity verification, HMAC) directly address this addressable specification. |

### §164.312(d) Person or Entity Authentication

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.312(d) | Person or Entity Authentication | R | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | Identity and credential management with MFA directly evidences person authentication requirements for ePHI systems. |
| §164.312(d) | Person or Entity Authentication | R | PR.AA-03 | Users and services are authenticated | Yes | full | Authentication requirements for all users and services directly evidence person and entity authentication for ePHI access. |

### §164.312(e)(1) Transmission Security

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.312(e)(1)(i) | Integrity Controls | A | PR.DS-02 | The confidentiality and integrity of data-in-transit are protected | Yes | full | TLS enforcement with integrity verification (authenticated encryption, HMAC) directly addresses ePHI transmission integrity controls. |
| §164.312(e)(1)(ii) | Encryption | A | PR.DS-02 | The confidentiality and integrity of data-in-transit are protected | Yes | full | TLS 1.2+ enforcement for all ePHI network communications directly evidences this addressable specification. |
| §164.312(e)(1)(ii) | Encryption | A | PR.IR-01 | Networks and environments are protected from unauthorized logical access | Yes | full | Network segmentation and access controls enforce encrypted-only transmission pathways for ePHI. |

---

## Organizational Requirements — §164.314

### §164.314(a)(2)(i) Business Associate Subcontractor Agreements

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.314(a)(2)(i) | Business Associate Subcontractor Agreements | R | GV.SC-01 | A cybersecurity supply chain risk management program is established | Yes | partial | Supply chain risk management addresses vendor security requirements; HIPAA additionally requires BAs to obtain BAAs from subcontractors and agents who access ePHI on their behalf. Subcontractor BAA existence is verified via Supplement Q5. |

---

## Breach Notification Rule — §164.400–414

### §164.410 Notification by Business Associates

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.410 | Notification by Business Associates | R | RS.CO-02 | Internal and external stakeholders are notified of incidents | Yes | partial | Stakeholder notification procedures address communication workflows; HIPAA requires BAs to notify CEs of breaches of unsecured ePHI without unreasonable delay and no later than 60 days from discovery, with specific required notification content. See Supplement Q6. |
| §164.410 | Notification by Business Associates | R | DE.AE-08 | Incidents are declared when adverse events meet defined incident criteria | Yes | partial | Incident declaration criteria establish the discovery event that starts the 60-day HIPAA notification clock. See Supplement Q6 for notification procedure documentation. |

### §164.412 Law Enforcement Delay

| HIPAA Section | Standard / Implementation Specification | Req/Addr | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|---|
| §164.412 | Law Enforcement Delay | R | RS.CO-02 | Internal and external stakeholders are notified of incidents | Yes | partial | Breach notification procedures should include a documented hold process for cases where law enforcement requests a delay in CE notification. Coverage note: verify breach notification procedure includes §164.412 provisions. See Supplement Q6. |

---

## Coverage Summary

| HIPAA Safeguard Category | Total Crosswalk Entries | Full | Partial | Gap | Advisory |
|---|---|---|---|---|---|
| Administrative Safeguards (§164.308) | | | | | |
| Physical Safeguards (§164.310) | | | | | |
| Technical Safeguards (§164.312) | | | | | |
| Organizational Requirements (§164.314) | | | | | |
| Breach Notification Rule (§164.400–414) | | | | | |
| **Total** | | | | | |

*Assessor populates counts after reviewing all rows above. Counts reflect crosswalk entries — a single implementation specification may have multiple rows mapping to different CSF subcategories.*

---

## Advisory Notes

### §164.308(a)(8) — Periodic Evaluation

This engagement satisfies the §164.308(a)(8) periodic evaluation requirement. The client should establish a recurring evaluation schedule — **annually is recommended** per industry practice. Document this engagement as the baseline evaluation and schedule the next assessment.

### §164.316(b)(2) — Documentation Retention

All policies, procedures, and records produced or reviewed during this assessment must be retained for a **minimum of 6 years** from the date of creation or the date when last in effect, whichever is later (45 CFR §164.316(b)(2)(i)). This is an administrative constraint, not an assessed gap.

---

*Authoritative sources: NIST CSF 2.0 (CSWP 29); 45 CFR Part 164 Subparts C (Security Rule) and D (Breach Notification Rule); HHS Guidance on HIPAA Security Rule (2022).*
