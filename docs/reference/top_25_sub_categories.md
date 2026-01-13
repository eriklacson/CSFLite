# CSFLite: Top 25 NIST CSF v2.0 Subcategories

These are the 25 most impactful and practical subcategories from NIST CSF v2.0, selected for the CSFLite framework. They span all six CSF Functions and are prioritized for SME/startup environments where lean security and rapid risk reduction matter most.

## Selection Criteria

1. **High impact-to-effort ratio** — maximum risk reduction with minimal overhead
2. **Automation potential** — can be partially or fully assessed via scanning tools
3. **Governance clarity** — clear yes/no/partial validation through questionnaires
4. **SME relevance** — addresses threats startups actually face (ransomware, credential theft, supply chain)

---

## GOVERN (GV) — 4 Subcategories

Governance sets the foundation. Without policy, roles, and risk awareness, technical controls are ad hoc.

### GV.PO-01 — Policy for managing cybersecurity risks is established based on organizational context, cybersecurity strategy, and priorities and is communicated and enforced

> **Why included:** Policy is the root of accountability. Even a one-page security policy beats having none.

### GV.RR-01 — Organizational leadership is responsible and accountable for cybersecurity risk and fosters a culture that is risk-aware, ethical, and continually improving

> **Why included:** Without clear ownership, security becomes everyone's and no one's job.

### GV.RM-01 — Risk management objectives are established and agreed to by organizational stakeholders

> **Why included:** Aligns security spending with business priorities. Prevents both under- and over-investment.

### GV.SC-01 — A cybersecurity supply chain risk management program, strategy, objectives, policies, and processes are established and agreed to by organizational stakeholders

> **Why included:** Third-party breaches are a leading cause of SME incidents. Vendor risk must be formalized.

---

## IDENTIFY (ID) — 5 Subcategories

You cannot protect what you don't know exists. Asset visibility is foundational.

### ID.AM-01 — Inventories of hardware managed by the organization are maintained

> **Why included:** Shadow IT and untracked devices are common attack vectors. Hardware inventory is non-negotiable.

### ID.AM-02 — Inventories of software, services, and systems managed by the organization are maintained

> **Why included:** Outdated software is a primary exploitation vector. You must know what's running.

### ID.AM-05 — Assets are prioritized based on classification, criticality, resources, and impact on the mission

> **Why included:** Not all assets are equal. Focus protection on crown jewels first.

### ID.RA-01 — Vulnerabilities in assets are identified, validated, and recorded

> **Why included:** Core to automated scanning workflows. Nuclei templates map directly here.

### ID.RA-05 — Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk and inform risk response prioritization

> **Why included:** Connects technical findings to business decisions. Essential for lean security.

---

## PROTECT (PR) — 6 Subcategories

Safeguards that prevent or limit impact. Emphasis on automatable controls and ransomware defense.

### PR.AA-01 — Identities and credentials for authorized users, services, and hardware are managed by the organization

> **Why included:** Credential compromise is the #1 initial access vector. Default credentials are trivially exploitable.

### PR.AA-03 — Users, services, and hardware are authenticated

> **Why included:** Authentication gaps (open admin panels, no MFA) are detectable via scanning.

### PR.DS-01 — The confidentiality, integrity, and availability of data-at-rest are protected

> **Why included:** Encryption at rest prevents data theft from stolen devices or breached storage.

### PR.DS-02 — The confidentiality, integrity, and availability of data-in-transit are protected

> **Why included:** TLS misconfigurations are automatable findings. Protects against MITM attacks.

### PR.DS-11 — Backups of data are created, protected, maintained, and tested

> **Why included:** **Critical for ransomware resilience.** Tested backups are the difference between recovery and paying ransom.

### PR.IR-01 — Networks and environments are protected from unauthorized logical access and usage

> **Why included:** Network segmentation, firewall rules, and secure protocols. Partially automatable via scanning.

---

## DETECT (DE) — 4 Subcategories

Finding attacks in progress or after the fact. CSFLite emphasizes detection because scanning IS detection.

### DE.CM-01 — Networks and network services are monitored to find potentially adverse events

> **Why included:** Network monitoring catches lateral movement and data exfiltration.

### DE.CM-09 — Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events

> **Why included:** Endpoint and application monitoring. Catches exploitation of vulnerabilities.

### DE.AE-02 — Potentially adverse events are analyzed to better understand associated activities

> **Why included:** Raw alerts aren't actionable. Analysis determines severity and scope.

### DE.AE-08 — Incidents are declared when adverse events meet the defined incident criteria

> **Why included:** Defines when a finding becomes an incident requiring response. Critical threshold.

---

## RESPOND (RS) — 4 Subcategories

Actions taken when incidents occur. Focused on containment, communication, and eradication.

### RS.MA-01 — The incident response plan is executed in coordination with relevant third parties once an incident is declared

> **Why included:** Having and testing an IR plan is the difference between chaos and controlled response.

### RS.CO-02 — Internal and external stakeholders are notified of incidents

> **Why included:** Communication failures during incidents cause reputational and legal damage.

### RS.MI-01 — Incidents are contained

> **Why included:** Containment limits blast radius. Speed matters.

### RS.MI-02 — Incidents are eradicated

> **Why included:** Removing threats prevents recurrence. Validates successful response.

---

## RECOVER (RC) — 2 Subcategories

Restoring operations after an incident. Lean selection — recovery is where tested backups pay off.

### RC.RP-01 — The recovery portion of the incident response plan is executed once initiated from the incident response process

> **Why included:** Recovery procedures must be documented and tested, not improvised.

### RC.CO-03 — Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders

> **Why included:** Stakeholders need status updates. Silence breeds panic and mistrust.

---

## Summary Table

| Function | Count | Subcategory IDs |
|----------|-------|-----------------|
| GOVERN | 4 | GV.PO-01, GV.RR-01, GV.RM-01, GV.SC-01 |
| IDENTIFY | 5 | ID.AM-01, ID.AM-02, ID.AM-05, ID.RA-01, ID.RA-05 |
| PROTECT | 6 | PR.AA-01, PR.AA-03, PR.DS-01, PR.DS-02, PR.DS-11, PR.IR-01 |
| DETECT | 4 | DE.CM-01, DE.CM-09, DE.AE-02, DE.AE-08 |
| RESPOND | 4 | RS.MA-01, RS.CO-02, RS.MI-01, RS.MI-02 |
| RECOVER | 2 | RC.RP-01, RC.CO-03 |
| **TOTAL** | **25** | |

---

## Automation Coverage

| Category | Fully Automatable | Partially Automatable | Manual Only |
|----------|-------------------|----------------------|-------------|
| GOVERN | 0 | 0 | 4 |
| IDENTIFY | 0 | 4 | 1 |
| PROTECT | 0 | 5 | 1 |
| DETECT | 0 | 4 | 0 |
| RESPOND | 0 | 0 | 4 |
| RECOVER | 0 | 0 | 2 |

**Automatable (full or partial): 13/25 (52%)**  
**Manual governance checks: 12/25 (48%)**

---

## What's NOT Included (and Why)

| Excluded | Rationale |
|----------|-----------|
| ID.AM-03 (Data flows) | Requires mature architecture documentation most SMEs lack |
| ID.AM-04 (Supplier inventory) | Covered implicitly by GV.SC-01 |
| PR.DS-10 (Integrity checking) | File integrity monitoring is operationally complex for SMEs |
| PR.AT-01/02 (Training) | Important but not automatable; assumes some baseline exists |
| RC.RP-02 through RC.RP-05 | Recovery granularity beyond SME needs; RC.RP-01 covers essentials |
| All GV.OC subcategories | Organizational context is implicit in policy (GV.PO-01) |

---

## Canonical Reference

All subcategory IDs and descriptions are aligned with:

**NIST Cybersecurity Framework (CSF) 2.0**  
NIST CSWP 29, February 26, 2024  
https://doi.org/10.6028/NIST.CSWP.29

---
