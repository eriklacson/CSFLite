# CSFLite Manual Questionnaire

Questionnaire covering CSF v2.0 subcategories from the CSFLite Top 25 that require manual validation. Designed for use alongside automated scan results for comprehensive assessment.

Each question includes:
- CSF Function and Subcategory ID (aligned with NIST CSF 2.0)
- Plain-language yes/no/partial question
- Examples of acceptable evidence

---

## GOVERN

### GV.PO-01 — Policy for managing cybersecurity risks is established

**Question:** Has a formal cybersecurity policy been established, approved by leadership, and communicated to the organization?

**Evidence:** 
- Security policy document with approval signatures
- Communication records (email, intranet posting)
- Staff acknowledgment records

**Scoring:**
- Yes: Policy exists, is approved, and communicated
- Partial: Policy exists but not formally approved or not communicated
- No: No documented policy

---

### GV.RR-01 — Organizational leadership is responsible for cybersecurity risk

**Question:** Is there a named individual or role with explicit accountability for cybersecurity, documented authority, and leadership support?

**Evidence:**
- Organizational chart showing security role
- Job description with security responsibilities
- Board or executive meeting minutes assigning accountability

**Scoring:**
- Yes: Named accountable party with documented authority
- Partial: Informal assignment without documentation
- No: No assigned accountability

---

### GV.RM-01 — Risk management objectives are established

**Question:** Are cybersecurity risk appetite and tolerance statements documented and agreed upon by organizational stakeholders?

**Evidence:**
- Risk appetite statement
- Board/executive approval of risk tolerance
- Risk register with accepted risk documentation

**Scoring:**
- Yes: Documented and approved risk appetite/tolerance
- Partial: Informal risk discussions without documentation
- No: No risk appetite defined

---

### GV.SC-01 — Supply chain risk management program is established

**Question:** Do you maintain security requirements for vendors and assess third-party cybersecurity risks?

**Evidence:**
- Vendor inventory with risk classifications
- Contracts with security clauses
- Third-party security assessments or questionnaires

**Scoring:**
- Yes: Formal vendor risk program with documented requirements
- Partial: Some vendor oversight but inconsistent
- No: No vendor security requirements

---

## IDENTIFY

### ID.AM-01 — Hardware inventories are maintained

**Question:** Do you maintain a current, accurate inventory of all hardware assets managed by the organization?

**Evidence:**
- Hardware asset inventory (spreadsheet, CMDB)
- Network discovery scan results
- Physical asset tags and tracking

**Scoring:**
- Yes: Complete, current inventory with regular updates
- Partial: Inventory exists but incomplete or outdated
- No: No hardware inventory

---

### ID.AM-02 — Software and systems inventories are maintained

**Question:** Do you maintain a current inventory of all software, services, and systems?

**Evidence:**
- Software inventory with versions
- License management records
- System documentation

**Scoring:**
- Yes: Complete software inventory with version tracking
- Partial: Partial inventory or outdated records
- No: No software inventory

---

### ID.AM-05 — Assets are prioritized by criticality

**Question:** Do you classify and prioritize assets based on business impact, criticality, and value?

**Evidence:**
- Asset classification scheme (critical/high/medium/low)
- Business Impact Analysis (BIA) documentation
- Criticality ratings in asset inventory

**Scoring:**
- Yes: Formal classification with documented criteria
- Partial: Informal prioritization without consistent criteria
- No: No asset prioritization

---

### ID.RA-05 — Risk prioritization informs response

**Question:** Do you use risk scoring methodology to prioritize vulnerability remediation and security investments?

**Evidence:**
- Risk scoring methodology documentation
- Prioritized remediation queue based on risk
- Risk register with likelihood/impact ratings

**Scoring:**
- Yes: Formal risk-based prioritization in use
- Partial: Some risk consideration but not systematic
- No: No risk-based prioritization

---

## PROTECT

### PR.DS-11 — Backups are created and tested

**Question:** Are backups performed regularly, stored securely (including offline/immutable copies), and restoration tested periodically?

**Evidence:**
- Backup schedule documentation
- Restoration test logs with success/failure records
- Backup verification reports
- Offsite/immutable backup configuration

**Scoring:**
- Yes: Regular backups with tested restoration and secure storage
- Partial: Backups exist but untested or insecure storage
- No: No backup program

---

## DETECT

### DE.CM-01 — Networks are monitored for adverse events

**Question:** Do you have network monitoring, IDS/IPS, or log analysis in place to detect potential security events?

**Evidence:**
- Network monitoring tool deployment
- IDS/IPS configuration
- Log aggregation and review procedures
- Alert rules and thresholds

**Scoring:**
- Yes: Active network monitoring with alerting
- Partial: Some logging but no active monitoring or alerting
- No: No network monitoring

---

### DE.CM-09 — Computing systems are monitored for adverse events

**Question:** Do you have endpoint detection, host-based monitoring, or application monitoring to detect security events?

**Evidence:**
- EDR/antivirus deployment status
- Host-based IDS configuration
- Application security monitoring
- Endpoint coverage metrics

**Scoring:**
- Yes: Comprehensive endpoint monitoring deployed
- Partial: Partial deployment or basic antivirus only
- No: No endpoint monitoring

---

### DE.AE-02 — Adverse events are analyzed

**Question:** Do you have a defined process to triage, analyze, and document security alerts?

**Evidence:**
- Alert triage procedures/SOP
- Analysis documentation examples
- Escalation procedures

**Scoring:**
- Yes: Documented triage process with consistent execution
- Partial: Ad hoc analysis without documented process
- No: No alert analysis process

---

### DE.AE-08 — Incidents are declared when criteria are met

**Question:** Are incident declaration criteria defined, documented, and understood by the security team?

**Evidence:**
- Incident classification matrix
- Severity level definitions
- Declaration procedure documentation

**Scoring:**
- Yes: Clear, documented incident criteria
- Partial: Informal understanding without documentation
- No: No incident criteria defined

---

## RESPOND

### RS.MA-01 — Incident response plan is executed

**Question:** Do you have a documented incident response plan that has been tested in the past 12 months?

**Evidence:**
- Incident response plan document
- Tabletop exercise reports
- Drill/simulation logs
- Post-exercise improvement actions

**Scoring:**
- Yes: Documented plan tested within 12 months
- Partial: Plan exists but untested or outdated
- No: No incident response plan

---

### RS.CO-02 — Stakeholders are notified of incidents

**Question:** Do you have defined communication procedures for notifying internal and external stakeholders during incidents?

**Evidence:**
- Incident communication plan
- Notification templates
- Stakeholder contact lists
- Regulatory notification requirements

**Scoring:**
- Yes: Documented communication procedures
- Partial: Informal communication without templates
- No: No communication procedures

---

### RS.MI-01 — Incidents are contained

**Question:** Do you have containment procedures and playbooks for common incident types?

**Evidence:**
- Containment playbooks
- Isolation procedures
- Network segmentation capabilities for containment

**Scoring:**
- Yes: Documented containment procedures
- Partial: Ad hoc containment capability
- No: No containment procedures

---

### RS.MI-02 — Incidents are eradicated

**Question:** Do you have procedures to remove threats and validate clean state after incidents?

**Evidence:**
- Eradication procedures
- Validation/verification checklists
- Malware removal procedures
- System rebuild procedures

**Scoring:**
- Yes: Documented eradication and validation procedures
- Partial: Informal eradication without validation
- No: No eradication procedures

---

## RECOVER

### RC.RP-01 — Recovery plan is executed

**Question:** Do you have documented recovery procedures that have been tested in the past 12 months?

**Evidence:**
- Recovery/DR plan document
- Restoration test logs
- RTO/RPO definitions and validation
- Recovery exercise reports

**Scoring:**
- Yes: Documented plan tested within 12 months
- Partial: Plan exists but untested
- No: No recovery plan

---

### RC.CO-03 — Recovery progress is communicated

**Question:** Do you have a communication plan for providing recovery status updates to stakeholders?

**Evidence:**
- Recovery communication plan
- Status update templates
- Stakeholder contact lists for recovery

**Scoring:**
- Yes: Documented recovery communication procedures
- Partial: Informal updates without structured plan
- No: No recovery communication plan

---

## Scoring Summary

| Response | Score | Interpretation |
|----------|-------|----------------|
| Yes | 1.0 | Full compliance with subcategory |
| Partial | 0.5 | Partial compliance; improvement needed |
| No | 0.0 | Non-compliant; gap identified |

**Gap Score Calculation:**  
`Gap Score = Weight × (1 - Response Score)`

Higher gap scores indicate greater risk exposure requiring prioritized remediation.

---

## Canonical Reference

All subcategory IDs and descriptions align with:

**NIST Cybersecurity Framework (CSF) 2.0**  
NIST CSWP 29, February 26, 2024  
https://doi.org/10.6028/NIST.CSWP.29

---
