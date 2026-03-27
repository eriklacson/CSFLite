# CSFLite to SOC 2 Trust Services Criteria Crosswalk

**Framework:** NIST CSF 2.0 (CSWP 29) → AICPA 2017 Trust Services Criteria (2022 revised points of focus)
**CSFLite version:** 1.0.0 (25 controls — see `csflite/controls.json`)
**Architectural basis:** [ADR-0001](../adr/ADR-0001-full-csf-crosswalk.md)
**Scope:** Security (CC1–CC9), Availability (A1), Confidentiality (C1)
**Excluded:** Processing Integrity, Privacy

**Coverage ratings:**
- `full` — CSF subcategory is in the CSFLite 25 and directly evidences the SOC 2 criterion
- `partial` — CSF subcategory is in the CSFLite 25 but only partially evidences the criterion, or a related CSFLite control provides indirect evidence
- `gap` — criterion maps to a CSF subcategory outside the CSFLite 25; addressed by `templates/soc2-supplement-questionnaire.csv`

---

## CC1 — Control Environment

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC1.1 | COSO Principle 1: Demonstrates commitment to integrity and ethical values | GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context and priorities | Yes | full | Cybersecurity policy formalizes leadership commitment and ethical obligations for information security. |
| CC1.1 | COSO Principle 1: Demonstrates commitment to integrity and ethical values | GV.RR-01 | Organizational leadership is responsible and accountable for cybersecurity risk | Yes | full | Named accountability for cybersecurity risk directly evidences leadership commitment to integrity. |
| CC1.2 | COSO Principle 2: Exercises oversight responsibility | GV.RR-01 | Organizational leadership is responsible and accountable for cybersecurity risk | Yes | full | Documented authority and ownership demonstrates board/leadership oversight of security risk. |
| CC1.2 | COSO Principle 2: Exercises oversight responsibility | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | full | Stakeholder-agreed risk management objectives evidence active oversight responsibility. |
| CC1.3 | COSO Principle 3: Establishes structure, authority, and responsibility | GV.RR-01 | Organizational leadership is responsible and accountable for cybersecurity risk | Yes | full | Documented roles, RACI, and authority structure directly map to this principle. |
| CC1.3 | COSO Principle 3: Establishes structure, authority, and responsibility | GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context and priorities | Yes | partial | Policy establishes authority but does not fully document organizational structure for control activities. |
| CC1.4 | COSO Principle 4: Demonstrates commitment to competence | GV.OC-04 | Organizational cybersecurity roles and responsibilities are coordinated and aligned with third-party stakeholders | No | gap | Competence requirements and training for security roles are outside CSFLite 25; see supplement questionnaire — Security Awareness (CC2) section. |
| CC1.5 | COSO Principle 5: Enforces accountability | GV.RR-01 | Organizational leadership is responsible and accountable for cybersecurity risk | Yes | full | Explicit named accountability with documented authority directly evidences enforcement of accountability. |
| CC1.5 | COSO Principle 5: Enforces accountability | GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context and priorities | Yes | partial | Policy defines expected behaviors but evidence of enforcement mechanisms (disciplinary procedures) must be documented separately. |

---

## CC2 — Communication and Information

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC2.1 | COSO Principle 13: Uses relevant information | DE.AE-02 | Potentially adverse events are analyzed to understand associated activities | Yes | partial | Event analysis produces relevant security information but does not address broader information quality and availability for control activities. |
| CC2.1 | COSO Principle 13: Uses relevant information | ID.RA-05 | Threats and vulnerabilities are used to understand inherent risk and prioritize response | Yes | partial | Risk-prioritized information feeds decision-making; partial because information management processes are broader than threat/vulnerability data. |
| CC2.2 | COSO Principle 14: Communicates internally | GV.OC-01 | The organizational mission is understood and informs cybersecurity risk management | No | gap | Internal communication of security policies and responsibilities to personnel is outside CSFLite 25; see supplement questionnaire — Security Awareness (CC2) section. |
| CC2.2 | COSO Principle 14: Communicates internally | PR.AT-01 | Awareness activities are provided | No | gap | Security awareness communication to all personnel is outside CSFLite 25; see supplement questionnaire — Security Awareness (CC2) section. |
| CC2.3 | COSO Principle 15: Communicates externally | GV.SC-01 | A cybersecurity supply chain risk management program is established | Yes | partial | Vendor security requirements in contracts address one dimension of external communication; broader external reporting obligations are a gap. |
| CC2.3 | COSO Principle 15: Communicates externally | RS.CO-02 | Internal and external stakeholders are notified of incidents | Yes | partial | Incident notification addresses reactive external communication; proactive external reporting (e.g., to regulators, customers) must be addressed separately. |

---

## CC3 — Risk Assessment

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC3.1 | COSO Principle 6: Specifies suitable objectives | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | full | Risk management objectives directly define the risk context against which deviations are assessed. |
| CC3.2 | COSO Principle 7: Identifies and analyzes risk | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Yes | full | Regular vulnerability identification and a maintained register directly evidence risk identification. |
| CC3.2 | COSO Principle 7: Identifies and analyzes risk | ID.RA-05 | Threats and vulnerabilities are used to understand inherent risk and prioritize response | Yes | full | Risk scoring methodology (likelihood × impact) directly evidences risk analysis and prioritization. |
| CC3.3 | COSO Principle 8: Assesses fraud risk | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | partial | General risk management framework provides context; specific fraud risk scenarios must be documented explicitly in the risk register. |
| CC3.3 | COSO Principle 8: Assesses fraud risk | ID.RA-05 | Threats and vulnerabilities are used to understand inherent risk and prioritize response | Yes | partial | Threat prioritization can encompass fraud vectors but only if insider threat and fraud scenarios are explicitly included in the organization's risk register. |
| CC3.4 | COSO Principle 9: Identifies and analyzes significant change | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Yes | partial | Vulnerability tracking captures one dimension of change-related risk; formal change management processes are outside CSFLite 25; see supplement questionnaire — Change Management (CC8) section. |
| CC3.4 | COSO Principle 9: Identifies and analyzes significant change | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | partial | Risk objectives should trigger reassessment on significant change, but change management controls are outside CSFLite 25; see supplement questionnaire — Change Management (CC8) section. |

---

## CC4 — Monitoring Activities

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC4.1 | COSO Principle 16: Conducts ongoing and/or separate evaluations | DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Yes | full | Continuous network monitoring directly evidences ongoing evaluation of control effectiveness. |
| CC4.1 | COSO Principle 16: Conducts ongoing and/or separate evaluations | DE.CM-09 | Computing hardware and software are monitored to find potentially adverse events | Yes | full | Endpoint monitoring provides ongoing evaluation of system-level controls. |
| CC4.1 | COSO Principle 16: Conducts ongoing and/or separate evaluations | DE.AE-02 | Potentially adverse events are analyzed to understand associated activities | Yes | full | Structured alert analysis with documented SLAs evidences evaluation rigor. |
| CC4.2 | COSO Principle 17: Evaluates and communicates deficiencies | DE.AE-08 | Incidents are declared when adverse events meet defined incident criteria | Yes | full | Incident declaration criteria formalize the escalation of identified deficiencies. |
| CC4.2 | COSO Principle 17: Evaluates and communicates deficiencies | RS.CO-02 | Internal and external stakeholders are notified of incidents | Yes | full | Stakeholder notification procedures ensure deficiencies are communicated to appropriate parties. |

---

## CC5 — Control Activities

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC5.1 | COSO Principle 10: Selects and develops control activities | GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context and priorities | Yes | full | Policy establishes the framework from which control activities are selected and applied. |
| CC5.1 | COSO Principle 10: Selects and develops control activities | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | IAM controls (password policy, MFA) are concrete, selected control activities. |
| CC5.1 | COSO Principle 10: Selects and develops control activities | PR.IR-01 | Networks and environments are protected from unauthorized logical access | Yes | full | Network segmentation and firewall rules are documented control activities for logical access. |
| CC5.2 | COSO Principle 11: Selects and develops general controls over technology | PR.DS-01 | The confidentiality and integrity of data-at-rest are protected | Yes | full | Encryption at rest is a general technology control directly in scope. |
| CC5.2 | COSO Principle 11: Selects and develops general controls over technology | PR.DS-02 | The confidentiality and integrity of data-in-transit are protected | Yes | full | TLS enforcement is a general technology control directly in scope. |
| CC5.2 | COSO Principle 11: Selects and develops general controls over technology | DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Yes | full | Network monitoring is a general technology control. |
| CC5.3 | COSO Principle 12: Deploys through policies and procedures | GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context and priorities | Yes | full | Formal policy deployed to all staff is the primary evidence for this principle. |
| CC5.3 | COSO Principle 12: Deploys through policies and procedures | PR.AA-03 | Users and services are authenticated | Yes | full | Authentication procedures deployed through documented policy and configuration evidence this principle. |

---

## CC6 — Logical and Physical Access Controls

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC6.1 | Logical access security software, infrastructure, and architectures | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | Identity and credential management directly addresses logical access security. |
| CC6.1 | Logical access security software, infrastructure, and architectures | PR.AA-03 | Users and services are authenticated | Yes | full | Authentication controls address logical access to infrastructure and applications. |
| CC6.1 | Logical access security software, infrastructure, and architectures | PR.IR-01 | Networks and environments are protected from unauthorized logical access | Yes | full | Network-level access controls (segmentation, firewalls) address logical access architecture. |
| CC6.2 | Prior to issuing system credentials and granting access | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | full | Credential management processes (provisioning, MFA enrollment) address pre-access controls. |
| CC6.3 | Role-based access controls | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | partial | IAM controls address identity management; explicit role-based access control (RBAC) implementation evidence must be documented separately. |
| CC6.4 | Restricts physical access | PR.AA-05 | Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed | No | gap | Physical access controls for facilities are outside CSFLite 25; see supplement questionnaire — Physical Access Controls (CC6.4) section. |
| CC6.4 | Restricts physical access | PR.AA-06 | Physical access to assets is managed, monitored, and enforced commensurate with risk | No | gap | Physical access monitoring and enforcement are outside CSFLite 25; see supplement questionnaire — Physical Access Controls (CC6.4) section. |
| CC6.5 | Discontinues logical and physical access | PR.AA-01 | Identities and credentials for authorized users and services are managed | Yes | partial | Credential management covers provisioning; deprovisioning/offboarding procedures must be explicitly documented as part of IAM evidence. |
| CC6.6 | Logical access security measures — external access | PR.AA-03 | Users and services are authenticated | Yes | full | Authentication requirements for remote and external access are covered. |
| CC6.6 | Logical access security measures — external access | PR.IR-01 | Networks and environments are protected from unauthorized logical access | Yes | full | Firewall rules and network segmentation address boundary controls for external access. |
| CC6.7 | Restricts transmission and movement of information | PR.DS-02 | The confidentiality and integrity of data-in-transit are protected | Yes | full | TLS enforcement and transit protection controls directly address information transmission security. |
| CC6.8 | Prevents or detects unauthorized or malicious software | DE.CM-09 | Computing hardware and software are monitored to find potentially adverse events | Yes | full | Endpoint monitoring and detection of unauthorized software changes address this criterion. |

---

## CC7 — System Operations

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC7.1 | Detects and monitors new vulnerabilities | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Yes | full | Regular vulnerability scanning and a maintained register directly address detection of new vulnerabilities. |
| CC7.1 | Detects and monitors new vulnerabilities | DE.CM-09 | Computing hardware and software are monitored to find potentially adverse events | Yes | full | Endpoint monitoring provides continuous detection of configuration changes and potential vulnerabilities. |
| CC7.2 | Monitors system components for anomalous behavior | DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Yes | full | Network monitoring for anomalous traffic directly evidences this criterion. |
| CC7.2 | Monitors system components for anomalous behavior | DE.CM-09 | Computing hardware and software are monitored to find potentially adverse events | Yes | full | Endpoint monitoring for anomalous behavior directly evidences this criterion. |
| CC7.3 | Evaluates security events | DE.AE-02 | Potentially adverse events are analyzed to understand associated activities | Yes | full | Structured analysis and triage of security alerts with documented SLAs directly evidence evaluation. |
| CC7.3 | Evaluates security events | DE.AE-08 | Incidents are declared when adverse events meet defined incident criteria | Yes | full | Incident declaration criteria formalize the evaluation-to-escalation threshold. |
| CC7.4 | Responds to identified security incidents | RS.MA-01 | The incident response plan is executed in coordination with relevant third parties | Yes | full | Tested IR plan with third-party coordination directly addresses incident response execution. |
| CC7.4 | Responds to identified security incidents | RS.MI-01 | Incidents are contained | Yes | full | Containment playbooks with isolation capability directly evidence response to incidents. |
| CC7.4 | Responds to identified security incidents | RS.MI-02 | Incidents are eradicated | Yes | full | Eradication procedures and validation steps complete the response lifecycle. |
| CC7.5 | Identifies, develops, and implements changes to recover | RC.RP-01 | The recovery portion of the incident response plan is executed | Yes | full | Recovery procedures with tested restoration evidence post-incident recovery capability. |
| CC7.5 | Identifies, develops, and implements changes to recover | RC.CO-03 | Recovery activities and progress are communicated to stakeholders | Yes | full | Stakeholder communication during recovery is documented and planned. |

---

## CC8 — Change Management

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC8.1 | Authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes | PR.PS-01 | Configuration management practices are established and applied | No | gap | Configuration management and change authorization processes are outside CSFLite 25; see supplement questionnaire — Change Management (CC8) section. |
| CC8.1 | Authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes | PR.PS-02 | Software is maintained, replaced, and removed commensurate with risk | No | gap | Software lifecycle management (patching, decommissioning) is outside CSFLite 25; see supplement questionnaire — Change Management (CC8) section. |
| CC8.1 | Authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes | PR.PS-04 | Logs are generated to enable monitoring, with appropriate log retention | No | gap | Audit logging for changes is outside CSFLite 25; see supplement questionnaire — Change Management (CC8) section. |
| CC8.1 | Authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes | PR.PS-06 | Secure software development practices are followed | No | gap | Secure SDLC and change approval workflows are outside CSFLite 25; see supplement questionnaire — Change Management (CC8) section. |
| CC8.1 | Authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes | ID.AM-02 | Inventories of software and systems managed by the organization are maintained | Yes | partial | Software inventory supports change awareness but does not constitute a change management control. |

---

## CC9 — Risk Mitigation

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| CC9.1 | Identifies, selects, and develops risk mitigation activities | ID.RA-05 | Threats and vulnerabilities are used to understand inherent risk and prioritize response | Yes | full | Risk-prioritized response selection directly evidences risk mitigation activity selection. |
| CC9.1 | Identifies, selects, and develops risk mitigation activities | GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Yes | full | Risk management framework with documented objectives provides the governance basis for mitigation selection. |
| CC9.2 | Assesses and manages risks from vendors and business partners | GV.SC-01 | A cybersecurity supply chain risk management program is established | Yes | full | Vendor inventory, security requirements in contracts, and third-party assessments directly address this criterion. |
| CC9.2 | Assesses and manages risks from vendors and business partners | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Yes | partial | Vulnerability identification should extend to vendor-managed assets; evidence of third-party vulnerability tracking must be documented in the risk register. |

---

## A1 — Availability

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| A1.1 | Maintains environmental protections and alternative processing | PR.DS-11 | Backups of data are created and tested | Yes | partial | Backup strategy (3-2-1, tested restoration) evidences data availability; environmental controls (power, cooling) and alternative processing site arrangements are outside CSFLite 25; see supplement questionnaire — Business Continuity (A1) section. |
| A1.1 | Maintains environmental protections and alternative processing | RC.RP-02 | Recovery actions are selected, scoped, prioritized, and performed | No | gap | Formal BCP with alternative processing arrangements is outside CSFLite 25; see supplement questionnaire — Business Continuity (A1) section. |
| A1.2 | Maintains backup and recovery consistent with objectives | PR.DS-11 | Backups of data are created and tested | Yes | full | 3-2-1 backup strategy with quarterly restoration testing and documented RTO/RPO directly addresses this criterion. |
| A1.2 | Maintains backup and recovery consistent with objectives | RC.RP-01 | The recovery portion of the incident response plan is executed | Yes | full | Recovery procedures with tested backup restoration and defined RTO/RPO directly evidence recovery objective alignment. |
| A1.2 | Maintains backup and recovery consistent with objectives | RC.RP-03 | The integrity of backups and other restoration assets is verified before using them in restoration | No | gap | Explicit pre-restoration integrity verification is outside CSFLite 25; see supplement questionnaire — Business Continuity (A1) section. |
| A1.3 | Tests recovery plan objectives | RC.RP-01 | The recovery portion of the incident response plan is executed | Yes | full | Annual recovery plan testing with documented results directly evidences this criterion. |
| A1.3 | Tests recovery plan objectives | RC.RP-04 | Critical mission functions and cybersecurity continuity are considered in recovery planning | No | gap | BCP scope definition for critical functions is outside CSFLite 25; see supplement questionnaire — Business Continuity (A1) section. |
| A1.3 | Tests recovery plan objectives | RC.RP-05 | The integrity of systems and organizational continuity are evaluated after a cybersecurity incident | No | gap | Post-incident continuity evaluation is outside CSFLite 25; see supplement questionnaire — Business Continuity (A1) section. |

---

## C1 — Confidentiality

| SOC 2 Criterion | Criterion Name | NIST CSF 2.0 Subcategory ID | Subcategory Name | In CSFLite 25? | Coverage Rating | Notes |
|---|---|---|---|---|---|---|
| C1.1 | Identifies and maintains confidential information | PR.DS-01 | The confidentiality and integrity of data-at-rest are protected | Yes | full | Encryption at rest with a documented policy directly evidences confidential information protection. |
| C1.1 | Identifies and maintains confidential information | PR.DS-02 | The confidentiality and integrity of data-in-transit are protected | Yes | full | TLS enforcement for all transmissions directly evidences confidential information protection in transit. |
| C1.1 | Identifies and maintains confidential information | ID.AM-05 | Assets are prioritized based on classification and criticality | Yes | full | Asset classification scheme identifies confidential information assets and applies appropriate protection. |
| C1.2 | Disposes of confidential information | PR.DS-03 | Assets are formally managed throughout removal, transfers, and disposition | No | gap | Formal data and media disposal procedures are outside CSFLite 25; see supplement questionnaire — Data Disposal (C1.2) section. |
| C1.2 | Disposes of confidential information | PR.DS-10 | The integrity of hardware and software are verified | No | gap | Hardware sanitization and verification prior to disposal is outside CSFLite 25; see supplement questionnaire — Data Disposal (C1.2) section. |

---

## Coverage Summary

| SOC 2 Category | Total Criteria | Full | Partial | Gap |
|---|---|---|---|---|
| CC1 — Control Environment | 5 | 4 | 1 | 1 |
| CC2 — Communication and Information | 3 | 0 | 2 | 2 |
| CC3 — Risk Assessment | 4 | 2 | 2 | 0 |
| CC4 — Monitoring Activities | 2 | 2 | 0 | 0 |
| CC5 — Control Activities | 3 | 3 | 0 | 0 |
| CC6 — Logical and Physical Access | 8 | 6 | 1 | 2 |
| CC7 — System Operations | 5 | 5 | 0 | 0 |
| CC8 — Change Management | 1 | 0 | 1 | 4 |
| CC9 — Risk Mitigation | 2 | 2 | 1 | 0 |
| A1 — Availability | 3 | 2 | 1 | 4 |
| C1 — Confidentiality | 2 | 2 | 0 | 2 |

> **Note:** Counts reflect crosswalk entries (a single criterion may have multiple rows mapping to different CSF subcategories). Gap count reflects distinct gap entries, not distinct criteria — one criterion can have multiple gap entries.

---

*Authoritative sources: NIST CSF 2.0 (CSWP 29); AICPA 2017 Trust Services Criteria for Security, Availability, and Confidentiality (revised points of focus, 2022).*
