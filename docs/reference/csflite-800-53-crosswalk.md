# CSFLite to SP 800-53 Rev 5 — Control Crosswalk

Maps all 25 CSFLite controls to their primary NIST SP 800-53 Rev 5 counterparts with assessment methods derived from SP 800-53A Rev 5.

## How to Read This Crosswalk

Each CSFLite control (a curated NIST CSF 2.0 subcategory) maps to two or more SP 800-53 Rev 5 controls. The assessment method column describes how an assessor evaluates the control using three methods:

| Method | Description |
|---|---|
| **Examine** | Review documents, records, configurations, and artifacts to confirm the control is documented and configured |
| **Interview** | Discuss with responsible personnel to verify understanding, awareness, and operational execution |
| **Test** | Directly observe or exercise the control to verify it operates as described |

Some 800-53 controls appear under multiple CSFLite entries (e.g., IR-4 maps to several Respond and Detect controls). In an SSP, each 800-53 control is documented once with a single implementation narrative, even if it satisfies multiple CSF subcategories.

CSFLite measures control coverage (Yes / Partial / No). SP 800-53 assessment determines Satisfied / Other Than Satisfied per control objective.

---

## Summary

| Function | Controls | Weight Range |
|---|---|---|
| Govern | 4 | 1.0 – 1.5 |
| Identify | 5 | 1.2 – 1.5 |
| Protect | 6 | 1.0 – 1.5 |
| Detect | 4 | 1.0 – 1.2 |
| Respond | 4 | 1.0 – 1.5 |
| Recover | 2 | 1.2 – 1.5 |

---

## GOVERN

### GV.PO-01 — Policy for managing cybersecurity risks is established based on organizational context and priorities

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| PL-1 | Policy and Procedures | Examine: cybersecurity policy document, approval records, distribution evidence. Interview: leadership on policy awareness. |
| PM-1 | Information Security Program Plan | Examine: security program plan document. Interview: CISO/security lead on plan updates and review cycle. |
| PM-9 | Risk Management Strategy | Examine: risk management strategy document. Interview: leadership on risk appetite and tolerance statements. |

### GV.RR-01 — Organizational leadership is responsible and accountable for cybersecurity risk

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| PM-2 | Information Security Program Leadership Role | Examine: organizational chart, role descriptions. Interview: designated security lead on authority and reporting. |
| PM-29 | Risk Management Program Leadership Roles | Examine: charter or memo assigning risk management responsibility. Interview: executive sponsor. |
| PL-1 | Policy and Procedures | Examine: policy showing leadership sign-off. Interview: leadership on accountability model. |

### GV.RM-01 — Risk management objectives are established and agreed to by organizational stakeholders

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| RA-1 | Risk Assessment Policy and Procedures | Examine: risk assessment policy, procedures document. Interview: risk owner on objectives and review cadence. |
| PM-9 | Risk Management Strategy | Examine: documented risk appetite/tolerance. Interview: stakeholders on agreement and awareness. |
| RA-3 | Risk Assessment | Examine: most recent risk assessment output. Interview: assessor on methodology and findings. |

### GV.SC-01 — A cybersecurity supply chain risk management program is established

**Weight:** 1.0

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| SR-1 | Supply Chain Risk Management Policy and Procedures | Examine: supply chain risk policy. Interview: procurement on vendor security requirements. |
| SA-4 | Acquisition Process | Examine: contracts with security clauses. Interview: procurement on evaluation criteria. |
| SR-3 | Supply Chain Controls and Processes | Examine: vendor inventory with risk ratings. Test: verify vendor review cycle is followed. |

---

## IDENTIFY

### ID.AM-01 — Inventories of hardware managed by the organization are maintained

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| CM-8 | System Component Inventory | Examine: hardware asset inventory. Test: sample reconciliation against network scan. Interview: asset owner on update frequency. |
| CM-8(1) | Updates During Installation and Removal | Test: verify inventory updates when assets are provisioned or decommissioned. |

### ID.AM-02 — Inventories of software and systems managed by the organization are maintained

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| CM-8 | System Component Inventory | Examine: software inventory including versions. Test: compare inventory against installed software scan. |
| CM-10 | Software Usage Restrictions | Examine: approved software list. Test: verify unauthorized software detection. |
| CM-11 | User-Installed Software | Examine: policy on user-installed software. Test: verify enforcement mechanism. |

### ID.AM-05 — Assets are prioritized based on classification and criticality

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| RA-2 | Security Categorization | Examine: asset classification records (FIPS 199 or equivalent). Interview: system owner on classification rationale. |
| SC-7(5) | Deny by Default / Allow by Exception | Examine: evidence that critical asset protections are applied based on classification tier. |
| PM-7 | Enterprise Architecture | Examine: architecture documentation showing asset tiers and protection alignment. |

### ID.RA-01 — Vulnerabilities in assets are identified and recorded

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| RA-5 | Vulnerability Monitoring and Scanning | Test: verify scans run at documented frequency. Examine: vulnerability scan reports and remediation tracking. |
| RA-5(2) | Update Vulnerabilities to Be Scanned | Examine: scanner plugin/signature update configuration. Test: verify signatures are current. |
| SI-2 | Flaw Remediation | Examine: patch management records. Test: sample verification that critical patches are applied within SLA. |

### ID.RA-05 — Threats and vulnerabilities are used to understand inherent risk and prioritize response

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| RA-3 | Risk Assessment | Examine: risk assessment methodology and output. Interview: risk owner on prioritization rationale. |
| RA-3(1) | Supply Chain Risk Assessment | Examine: supply chain risk assessment (if applicable). Interview: procurement lead. |
| PM-16 | Threat Awareness Program | Examine: threat intelligence sources and consumption process. Interview: security lead on threat briefings. |

---

## PROTECT

### PR.AA-01 — Identities and credentials for authorized users and services are managed

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| AC-2 | Account Management | Examine: user account list, provisioning/deprovisioning records. Test: verify quarterly access review completion. Interview: admin on account lifecycle. |
| IA-2 | Identification and Authentication (Org Users) | Test: verify SSO/MFA enforcement. Examine: authentication configuration. Interview: identity team on bypass accounts. |
| IA-5 | Authenticator Management | Examine: password policy, MFA enrollment records. Test: verify credential rotation for service accounts. |

### PR.AA-03 — Users and services are authenticated

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| IA-2 | Identification and Authentication (Org Users) | Test: attempt login without MFA. Examine: Conditional Access/MFA policy. Interview: admin on exceptions. |
| IA-2(1) | Multi-Factor Authentication to Privileged Accounts | Test: verify MFA on all admin accounts. Examine: MFA policy scope. |
| IA-2(2) | Multi-Factor Authentication to Non-Privileged Accounts | Test: verify MFA on standard user accounts. Examine: policy enforcement evidence. |
| IA-8 | Identification and Authentication (Non-Org Users) | Examine: external user authentication mechanism. Test: verify enforcement for non-employee access. |

### PR.DS-01 — The confidentiality and integrity of data-at-rest are protected

**Weight:** 1.0

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| SC-28 | Protection of Information at Rest | Test: verify encryption is enabled on databases and storage. Examine: encryption configuration and key management. |
| SC-28(1) | Cryptographic Protection | Examine: encryption algorithm and key length. Test: verify keys are managed via HSM or key vault. |

### PR.DS-02 — The confidentiality and integrity of data-in-transit are protected

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| SC-8 | Transmission Confidentiality and Integrity | Test: TLS configuration scan (protocol version, cipher suites). Examine: TLS policy documentation. |
| SC-8(1) | Cryptographic Protection | Test: verify TLS 1.2+ enforcement, no fallback to deprecated protocols. Examine: certificate management. |
| SC-23 | Session Authenticity | Test: verify session tokens are transmitted over encrypted channels. Examine: session management configuration. |

### PR.DS-11 — Backups of data are created and tested

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| CP-9 | System Backup | Examine: backup configuration (scope, frequency, retention). Test: verify backup exists for critical systems. Interview: admin on backup monitoring. |
| CP-9(1) | Testing for Reliability and Integrity | Examine: backup restoration test records. Test: perform sample restoration and validate data integrity. |
| CP-6 | Alternate Storage Site | Examine: offsite/geo-redundant backup storage configuration. Interview: admin on DR storage strategy. |

### PR.IR-01 — Networks and environments are protected from unauthorized logical access

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| SC-7 | Boundary Protection | Examine: firewall rules, NSG/security group configuration. Test: verify deny-by-default posture. Interview: network admin on rule review cadence. |
| SC-7(5) | Deny by Default / Allow by Exception | Test: verify default-deny rules on perimeter and internal segmentation points. |
| AC-4 | Information Flow Enforcement | Examine: data flow rules between security zones. Test: verify enforcement of flow restrictions. |

---

## DETECT

### DE.CM-01 — Networks and network services are monitored to find potentially adverse events

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| SI-4 | System Monitoring | Examine: monitoring tool configuration, alert rules. Test: verify flow logs are enabled on all subnets. Interview: SOC/platform team on monitoring coverage. |
| SI-4(4) | Inbound and Outbound Communications Traffic | Test: verify both ingress and egress traffic are monitored. Examine: IDS/IPS deployment. |
| AU-6 | Audit Record Review, Analysis, and Reporting | Examine: log review procedures and frequency. Interview: reviewer on triage process. Test: verify alert-to-response timeline. |

### DE.CM-09 — Computing hardware and software are monitored to find potentially adverse events

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| SI-4 | System Monitoring | Examine: endpoint monitoring/EDR configuration. Test: verify agent deployment across fleet. Interview: security ops on detection rules. |
| SI-7 | Software, Firmware, and Information Integrity | Test: verify file integrity monitoring on critical binaries. Examine: FIM configuration and alert rules. |
| CM-3 | Configuration Change Control | Examine: change detection alerts. Test: verify unauthorized configuration changes trigger alerts. |

### DE.AE-02 — Potentially adverse events are analyzed to understand associated activities

**Weight:** 1.0

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| IR-4 | Incident Handling | Examine: incident triage procedures and SLAs. Interview: analyst on analysis workflow. Examine: sample incident analysis documentation. |
| SI-4 | System Monitoring | Examine: alert correlation rules and triage runbooks. Interview: SOC on false positive rate and tuning. |
| AU-6(1) | Automated Process Integration | Examine: SIEM correlation rules. Test: verify automated alert enrichment pipeline. |

### DE.AE-08 — Incidents are declared when adverse events meet defined incident criteria

**Weight:** 1.0

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| IR-4 | Incident Handling | Examine: incident declaration criteria (severity definitions). Interview: analyst on escalation decision process. |
| IR-5 | Incident Monitoring | Examine: incident tracking system/log. Test: verify incidents are tracked with timestamps and status. |
| IR-6 | Incident Reporting | Examine: reporting procedures and notification timelines. Interview: incident commander on reporting chain. |

---

## RESPOND

### RS.MA-01 — The incident response plan is executed in coordination with relevant third parties

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| IR-1 | Incident Response Policy and Procedures | Examine: IR policy and plan document. Interview: IR lead on plan awareness and distribution. |
| IR-4 | Incident Handling | Examine: recent incident records showing plan execution. Interview: IR team on coordination with third parties. |
| IR-8 | Incident Response Plan | Examine: IR plan (roles, escalation, contacts, playbooks). Test: verify plan has been tested via tabletop in past 12 months. |

### RS.CO-02 — Internal and external stakeholders are notified of incidents

**Weight:** 1.0

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| IR-6 | Incident Reporting | Examine: notification procedures, contact lists, templates. Interview: IR lead on regulatory notification requirements. |
| IR-6(1) | Automated Reporting | Examine: automated notification configuration (if implemented). Test: verify notification triggers. |
| IR-7 | Incident Response Assistance | Examine: agreements with external IR resources (MSSP, legal, forensics). Interview: IR lead on external coordination. |

### RS.MI-01 — Incidents are contained

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| IR-4 | Incident Handling | Examine: containment procedures/playbooks. Interview: IR team on containment options. Test: verify technical ability to isolate a system. |
| IR-4(1) | Automated Incident Handling Processes | Examine: automated containment capabilities (e.g., EDR auto-isolate). Test: verify automated response triggers. |
| SC-7 | Boundary Protection | Examine: ability to modify firewall/NSG rules for emergency containment. Test: verify emergency change process. |

### RS.MI-02 — Incidents are eradicated

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| IR-4 | Incident Handling | Examine: eradication procedures. Interview: IR team on clean-state validation process. |
| SI-3 | Malicious Code Protection | Examine: malware scanning/EDR capability. Test: verify full-scan capability on affected systems. |
| SI-2 | Flaw Remediation | Examine: process for patching exploited vulnerabilities during incident. Test: verify emergency patching capability. |

---

## RECOVER

### RC.RP-01 — The recovery portion of the incident response plan is executed

**Weight:** 1.5

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| CP-10 | System Recovery and Reconstitution | Examine: recovery procedures. Test: verify restoration from backup. Interview: admin on RTO/RPO targets. |
| CP-2 | Contingency Plan | Examine: contingency plan document. Interview: plan owner on test results and lessons learned. |
| IR-4 | Incident Handling | Examine: post-incident recovery records. Interview: IR team on recovery validation steps. |

### RC.CO-03 — Recovery activities and progress are communicated to stakeholders

**Weight:** 1.2

| 800-53 Control | Control Name | Assessment Method |
|---|---|---|
| CP-2 | Contingency Plan | Examine: communication plan within contingency plan. Interview: plan owner on stakeholder notification procedures. |
| IR-6 | Incident Reporting | Examine: post-incident reporting procedures. Interview: IR lead on lessons-learned distribution. |
| CP-4 | Contingency Plan Testing | Examine: test results and after-action reports. Interview: participants on communication effectiveness during exercises. |

---

## References

- NIST SP 800-53 Rev 5 — Security and Privacy Controls for Information Systems and Organizations
- NIST SP 800-53A Rev 5 — Assessing Security and Privacy Controls in Information Systems and Organizations
- NIST SP 800-53B — Control Baselines for Information Systems and Organizations
- NIST Cybersecurity Framework 2.0 (CSWP 29)
- CSFLite — github.com/eriklacson/CSFLite

---

*This crosswalk maps to primary 800-53 controls. Additional control enhancements may apply depending on FIPS 199 categorization and baseline selection. Assessment methods are derived from SP 800-53A Rev 5 assessment procedures.*
