# CSFLite: Automatable CSF Subcategories

This document identifies which CSFLite Top 25 subcategories can be fully or partially automated using vulnerability scanning tools (e.g., Nuclei) versus those requiring manual governance validation.

---

## Automation Classification

| Level | Definition |
|-------|------------|
| **Full** | Can be completely assessed via automated scanning |
| **Partial** | Some aspects automatable; others require manual validation |
| **Manual** | Requires human judgment, documentation review, or interviews |

---

## IDENTIFY Function

### ID.AM-01 — Hardware inventories are maintained *(Partial)*

**Automatable aspects:**
- Network discovery scans detect active hosts
- Port scans identify device types (printers, routers, servers)
- MAC address collection

**Manual aspects:**
- Offline/powered-off devices
- Physical asset verification
- Ownership and location tracking

**Tools:** Nmap, Nuclei network templates, asset discovery scanners

---

### ID.AM-02 — Software and systems inventories are maintained *(Partial)*

**Automatable aspects:**
- Service detection reveals running software
- Version fingerprinting identifies installed applications
- Cloud asset enumeration via API

**Manual aspects:**
- License compliance verification
- Business purpose documentation
- Decommissioning status

**Tools:** Nuclei technology detection templates, software composition analysis

---

### ID.AM-05 — Assets are prioritized by criticality *(Manual)*

**Why manual:** Criticality is a business judgment based on revenue impact, regulatory requirements, and operational dependencies. No scanner can determine business value.

**Evidence required:** Asset classification scheme, BIA documentation

---

### ID.RA-01 — Vulnerabilities are identified and recorded *(Full)*

**Fully automatable:** This is the core use case for vulnerability scanning.

**Nuclei template categories:**
- `cves/` — Known CVE detection
- `technologies/` — Version detection for outdated software
- `exposures/` — Credential and data exposures
- `misconfigurations/` — Security misconfigurations

**Tools:** Nuclei, Nessus, OpenVAS, Qualys

---

### ID.RA-05 — Risk prioritization informs response *(Manual)*

**Why manual:** Risk scoring requires combining technical severity with business context (asset criticality, threat likelihood, compensating controls).

**Partial automation:** CVSS scores provide technical severity; CSFLite heatmap scoring automates weighted prioritization.

---

## PROTECT Function

### PR.AA-01 — Identities and credentials are managed *(Partial)*

**Automatable aspects:**
- Default credential detection (`default-logins/` templates)
- Weak password policy indicators
- Exposed credentials in code/configs

**Manual aspects:**
- MFA enrollment verification
- Privileged access review
- Credential rotation compliance

**Tools:** Nuclei default-logins templates, credential scanners

---

### PR.AA-03 — Users and services are authenticated *(Partial)*

**Automatable aspects:**
- Unauthenticated admin panel detection (`auth/open-admin`)
- Anonymous access detection (FTP, SMB, databases)
- Missing authentication on APIs

**Manual aspects:**
- Authentication policy compliance
- Service account management
- Session management review

**Tools:** Nuclei auth templates, API security scanners

---

### PR.DS-01 — Data-at-rest is protected *(Partial)*

**Automatable aspects:**
- Directory listing exposure
- Backup file exposure
- Database exposure without authentication

**Manual aspects:**
- Disk encryption verification
- Database encryption configuration
- Key management practices

**Tools:** Nuclei exposure templates, directory brute-forcing

---

### PR.DS-02 — Data-in-transit is protected *(Full)*

**Fully automatable:** TLS/SSL configuration is entirely scannable.

**Automatable checks:**
- Certificate validity (expiration, chain, self-signed)
- Protocol versions (TLS 1.0/1.1 deprecated)
- Cipher suite strength
- HSTS header presence
- Certificate transparency

**Tools:** Nuclei SSL templates, testssl.sh, SSLyze

---

### PR.DS-11 — Backups are created and tested *(Manual)*

**Why manual:** Backup existence and restoration success cannot be determined externally.

**Evidence required:** Backup schedules, restoration test logs, RTO/RPO validation

---

### PR.IR-01 — Networks are protected from unauthorized access *(Partial)*

**Automatable aspects:**
- Open port enumeration
- Unnecessary service detection
- Firewall rule bypass testing

**Manual aspects:**
- Network segmentation verification
- Firewall rule documentation review
- Architecture compliance

**Tools:** Nuclei networking templates, Nmap, firewall scanners

---

## DETECT Function

### DE.CM-01 — Networks are monitored for adverse events *(Manual)*

**Why manual:** Monitoring capability requires verifying tool deployment, alert configuration, and operational processes.

**Partial automation:** Can detect if monitoring agents are running on scanned hosts.

---

### DE.CM-09 — Computing systems are monitored for adverse events *(Manual)*

**Why manual:** Similar to DE.CM-01; requires verification of endpoint detection deployment and configuration.

---

### DE.AE-02 — Adverse events are analyzed *(Manual)*

**Why manual:** Analysis quality depends on human processes, not technical controls.

**Evidence required:** Alert triage SOPs, analysis documentation

---

### DE.AE-08 — Incidents are declared when criteria are met *(Manual)*

**Why manual:** Incident criteria are policy decisions requiring documented thresholds.

**Evidence required:** Incident classification matrix, severity definitions

---

## RESPOND Function

### RS.MA-01 — Incident response plan is executed *(Manual)*

**Why manual:** Plan existence and testing require documentation review.

**Evidence required:** IR plan, tabletop exercise reports

---

### RS.CO-02 — Stakeholders are notified of incidents *(Manual)*

**Why manual:** Communication procedures are policy and process.

**Evidence required:** Communication plan, notification templates

---

### RS.MI-01 — Incidents are contained *(Manual)*

**Why manual:** Containment capability requires playbook review and capability assessment.

---

### RS.MI-02 — Incidents are eradicated *(Manual)*

**Why manual:** Eradication procedures and validation are process-dependent.

---

## RECOVER Function

### RC.RP-01 — Recovery plan is executed *(Manual)*

**Why manual:** Recovery capability requires documentation and test evidence.

**Evidence required:** Recovery plan, restoration test logs

---

### RC.CO-03 — Recovery progress is communicated *(Manual)*

**Why manual:** Communication procedures are policy-based.

---

## Summary

| Automation Level | Count | Subcategories |
|------------------|-------|---------------|
| **Full** | 2 | ID.RA-01, PR.DS-02 |
| **Partial** | 7 | ID.AM-01, ID.AM-02, PR.AA-01, PR.AA-03, PR.DS-01, PR.IR-01, ID.RA-05 |
| **Manual** | 16 | All GOVERN, DETECT (most), RESPOND, RECOVER + ID.AM-05, PR.DS-11 |

**Scan Coverage:** 9/25 subcategories (36%) have automatable components  
**Governance Coverage:** 25/25 subcategories (100%) assessable via questionnaire

---

## Nuclei Template Mapping

| CSF Subcategory | Primary Nuclei Template Categories |
|-----------------|-----------------------------------|
| ID.AM-02 | `technologies/`, `networking/` |
| ID.RA-01 | `cves/`, `vulnerabilities/`, `exposures/` |
| PR.AA-01 | `default-logins/` |
| PR.AA-03 | `auth/`, `misconfiguration/` |
| PR.DS-01 | `exposures/`, `misconfiguration/` |
| PR.DS-02 | `ssl/`, `headers/` |
| PR.IR-01 | `networking/`, `misconfiguration/` |

---
