# CSFLite Remediation Guidance

Actionable remediation guidance for each of the CSFLite Top 25 subcategories. Use it after the governance assessment flags a gap. The `recommendation` column in the assessment output is the one-line summary; this document expands it into steps.

---

## GOVERN

### GV.PO-01 — Policy for managing cybersecurity risks is established

**Gap Indicator:** No formal policy, or policy not communicated

**Remediation Steps:**
1. Draft a cybersecurity policy covering scope, roles, acceptable use, and enforcement
2. Obtain executive/board approval with documented sign-off
3. Communicate policy to all staff via email and intranet
4. Require acknowledgment from all employees
5. Schedule annual policy review

**Quick Win:** Start with a 1-2 page policy covering essentials; iterate over time.

**Resources:** SANS policy templates, NIST SP 800-53 (PL family)

---

### GV.RR-01 — Organizational leadership is responsible for cybersecurity risk

**Gap Indicator:** No named accountable party for security

**Remediation Steps:**
1. Designate a security lead (can be part-time role in small orgs)
2. Document role and authority in job description or charter
3. Ensure executive sponsorship and board awareness
4. Establish reporting cadence (monthly security updates to leadership)
5. Include cybersecurity in performance objectives

**Quick Win:** Name someone accountable today; formalize documentation within 30 days.

---

### GV.RM-01 — Risk management objectives are established

**Gap Indicator:** No documented risk appetite or tolerance

**Remediation Steps:**
1. Facilitate risk appetite discussion with leadership
2. Document acceptable risk levels (e.g., "no critical vulnerabilities on internet-facing systems")
3. Define risk tolerance thresholds for escalation
4. Integrate risk appetite into vulnerability management decisions
5. Review and update annually or after significant incidents

**Quick Win:** Define 3-5 risk statements leadership agrees to.

---

### GV.SC-01 — Supply chain risk management program is established

**Gap Indicator:** No vendor security requirements or tracking

**Remediation Steps:**
1. Create vendor inventory listing all third parties with data access
2. Classify vendors by risk tier (critical, high, medium, low)
3. Add security clauses to contracts (data protection, breach notification, audit rights)
4. Require security questionnaires for critical vendors
5. Schedule periodic vendor reviews (annual for critical, every 2 years for others)

**Quick Win:** Inventory your top 10 vendors and add security requirements to new contracts.

---

## IDENTIFY

### ID.AM-01 — Hardware inventories are maintained

**Gap Indicator:** No hardware inventory or outdated records

**Remediation Steps:**
1. Run network discovery scan to identify all connected devices
2. Create spreadsheet or CMDB with: device name, type, IP/MAC, owner, location, criticality
3. Implement process for adding new devices to inventory
4. Schedule quarterly inventory reconciliation
5. Tag physical assets for tracking

**Quick Win:** Export DHCP leases and network scan results as starting inventory.

---

### ID.AM-02 — Software and systems inventories are maintained

**Gap Indicator:** No software inventory or unknown installations

**Remediation Steps:**
1. Deploy software inventory tool or use endpoint agent reports
2. Document all approved software with versions
3. Flag unauthorized or end-of-life software for remediation
4. Establish software approval process
5. Schedule monthly software inventory review

**Quick Win:** Use existing endpoint agents (antivirus, MDM) to export software lists.

---

### ID.AM-05 — Assets are prioritized by criticality

**Gap Indicator:** All assets treated equally; no criticality classification

**Remediation Steps:**
1. Define classification scheme (Critical, High, Medium, Low)
2. Conduct Business Impact Analysis (BIA) for key systems
3. Assign criticality based on: revenue impact, data sensitivity, regulatory requirements
4. Document criticality in asset inventory
5. Use criticality to prioritize security controls and patching

**Quick Win:** Identify your top 10 crown jewel systems and mark them critical.

---

### ID.RA-01 — Vulnerabilities are identified and recorded

**Gap Indicator:** No regular vulnerability scanning, or findings not tracked

**Remediation Steps:**
1. Choose a scanner suited to your environment (external, internal, cloud, or container image)
2. Scan internet-facing systems at least monthly and after major changes
3. Record every finding in a vulnerability register with owner and status
4. Validate high and critical findings to remove false positives
5. Track each finding to closure and re-scan to confirm the fix

**Quick Win:** Run one external scan of your public IPs and domains this week and log the results.

---

### ID.RA-05 — Risk prioritization informs response

**Gap Indicator:** Vulnerabilities remediated randomly or by CVSS alone

**Remediation Steps:**
1. Define risk scoring methodology combining severity + asset criticality + exploitability
2. Create prioritized remediation queue
3. Set SLAs by risk tier (Critical: 24h, High: 7d, Medium: 30d, Low: 90d)
4. Track remediation against SLAs
5. Report risk trends to leadership

**Quick Win:** Multiply CVSS score by asset criticality weight for simple risk ranking.

---

## PROTECT

### PR.AA-01 — Identities and credentials are managed

**Gap Indicator:** Weak or shared passwords, no MFA, default credentials in use

**Remediation Steps:**
1. Publish a password policy (length over complexity; no reuse; password manager encouraged)
2. Enforce MFA for all privileged, remote, and email/SSO access
3. Remove or change all default credentials on devices and services
4. Give every person and service its own account; eliminate shared logins
5. Review accounts quarterly and disable leavers on their last day

**Quick Win:** Turn on MFA for your identity provider and email admin accounts today.

---

### PR.AA-03 — Users and services are authenticated

**Gap Indicator:** Admin panels, APIs, or file shares reachable without login

**Remediation Steps:**
1. List every administrative interface (cloud consoles, routers, CMS admin, databases)
2. Require authentication on each one; remove anonymous and guest access
3. Restrict admin interfaces to VPN or trusted IP ranges where possible
4. Use service accounts or API keys with least privilege for machine-to-machine access
5. Review authentication logs for failed or unexpected access

**Quick Win:** Check that no admin panel or database port is open to the internet without a login.

---

### PR.DS-01 — Data-at-rest is protected

**Gap Indicator:** Unencrypted laptops, databases, or storage holding sensitive data

**Remediation Steps:**
1. Identify where sensitive data is stored (endpoints, databases, cloud buckets, backups)
2. Enable full-disk encryption on all laptops and desktops
3. Enable encryption on databases and cloud storage
4. Store encryption keys separately from the data, using a managed key service where available
5. Block public access on cloud storage buckets by default

**Quick Win:** Confirm full-disk encryption is on for every company laptop.

---

### PR.DS-02 — Data-in-transit is protected

**Gap Indicator:** Plain HTTP, outdated TLS versions, or expired certificates

**Remediation Steps:**
1. Enforce TLS 1.2 or later on all websites, APIs, and mail servers
2. Disable SSL, TLS 1.0, TLS 1.1, and weak cipher suites
3. Redirect HTTP to HTTPS and enable HSTS
4. Keep a certificate inventory with expiry dates; automate renewal
5. Replace insecure protocols (FTP, Telnet) with secure alternatives (SFTP, SSH)

**Quick Win:** Run a free TLS check against your public domains and fix any grade below A.

---

### PR.DS-11 — Backups are created and tested

**Gap Indicator:** No backups, untested backups, or all backups online

**Remediation Steps:**
1. Implement 3-2-1 backup strategy: 3 copies, 2 media types, 1 offsite
2. Include immutable or offline backup copy (ransomware protection)
3. Automate backup schedules for all critical systems
4. Test restoration quarterly; document success/failure
5. Define and validate RTO/RPO targets

**Quick Win:** Verify you have at least one offline/immutable backup of critical data.

**Critical:** Untested backups are not backups. Schedule restoration test this quarter.

---

### PR.IR-01 — Networks are protected from unauthorized access

**Gap Indicator:** Flat network, undocumented firewall rules, unnecessary open ports

**Remediation Steps:**
1. Draw a simple network diagram showing zones (office, production, guest)
2. Separate production, office, and guest networks
3. Default-deny inbound firewall rules; allow only what is needed and document why
4. Close unused ports and disable unnecessary services
5. Review firewall and security group rules quarterly

**Quick Win:** Put guest Wi-Fi on its own network, isolated from company systems.

---

## DETECT

### DE.CM-01 — Networks are monitored for adverse events

**Gap Indicator:** No network monitoring or log analysis

**Remediation Steps:**
1. Deploy network monitoring tool (open source: Zeek, Suricata; commercial: various)
2. Aggregate logs from firewalls, routers, and critical systems
3. Define alerting rules for suspicious activity
4. Establish log retention (minimum 90 days, ideally 1 year)
5. Assign responsibility for alert review

**Quick Win:** Enable logging on perimeter firewall and review weekly.

---

### DE.CM-09 — Computing systems are monitored for adverse events

**Gap Indicator:** No endpoint detection or host monitoring

**Remediation Steps:**
1. Deploy EDR or enhanced antivirus on all endpoints
2. Enable host-based logging (Windows Event Logs, syslog)
3. Forward logs to central location
4. Configure alerts for critical events (failed logins, privilege escalation)
5. Monitor deployment coverage (target: 100% of managed endpoints)

**Quick Win:** Verify antivirus is deployed on all endpoints with current definitions.

---

### DE.AE-02 — Adverse events are analyzed

**Gap Indicator:** Alerts ignored or handled inconsistently

**Remediation Steps:**
1. Document alert triage procedure with severity classification
2. Define response SLAs by alert severity
3. Create runbooks for common alert types
4. Track alert volume and false positive rates
5. Tune alerts to reduce noise

**Quick Win:** Create a simple triage checklist: severity, affected systems, potential impact, escalation criteria.

---

### DE.AE-08 — Incidents are declared when criteria are met

**Gap Indicator:** No clear definition of what constitutes an incident

**Remediation Steps:**
1. Define incident severity levels (Critical, High, Medium, Low)
2. Document criteria for each level (e.g., data breach = Critical, phishing click = Medium)
3. Specify who can declare incidents
4. Create incident declaration checklist
5. Train team on incident criteria

**Quick Win:** Define 3-5 scenarios that automatically qualify as incidents.

---

## RESPOND

### RS.MA-01 — Incident response plan is executed

**Gap Indicator:** No IR plan or plan never tested

**Remediation Steps:**
1. Create incident response plan covering: detection, containment, eradication, recovery, lessons learned
2. Define roles and responsibilities (incident commander, technical lead, communications)
3. Include contact lists and escalation paths
4. Conduct tabletop exercise within 90 days
5. Update plan based on exercise findings

**Quick Win:** Start with a 2-page IR plan covering who to call and initial containment steps.

**Resources:** NIST SP 800-61 (Computer Security Incident Handling Guide)

---

### RS.CO-02 — Stakeholders are notified of incidents

**Gap Indicator:** No communication plan for incidents

**Remediation Steps:**
1. Identify stakeholders requiring notification (executives, legal, PR, customers, regulators)
2. Define notification triggers and timelines
3. Create communication templates for common scenarios
4. Designate spokesperson for external communications
5. Document regulatory notification requirements (GDPR: 72h, etc.)

**Quick Win:** Create stakeholder contact list with notification triggers.

---

### RS.MI-01 — Incidents are contained

**Gap Indicator:** No containment procedures or capabilities

**Remediation Steps:**
1. Document containment options: network isolation, account disable, system shutdown
2. Create playbooks for common incident types (malware, unauthorized access, data breach)
3. Verify technical capabilities exist (can you isolate a system quickly?)
4. Pre-authorize containment actions to avoid delays
5. Test containment procedures in exercises

**Quick Win:** Verify you can isolate a compromised system from the network within 30 minutes.

---

### RS.MI-02 — Incidents are eradicated

**Gap Indicator:** Threats removed incompletely or systems restored without validation

**Remediation Steps:**
1. Document eradication procedures for common threats
2. Create validation checklist (malware scans, IOC checks, log review)
3. Define clean state criteria before returning to production
4. Preserve evidence before eradication
5. Document post-eradication validation

**Quick Win:** Create a "return to production" checklist requiring security sign-off.

---

## RECOVER

### RC.RP-01 — Recovery plan is executed

**Gap Indicator:** No recovery plan or untested procedures

**Remediation Steps:**
1. Document recovery procedures for critical systems
2. Define Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO)
3. Test recovery procedures annually (minimum)
4. Document recovery dependencies (order of restoration)
5. Update procedures based on test results

**Quick Win:** Document recovery steps for your single most critical system.

---

### RC.CO-03 — Recovery progress is communicated

**Gap Indicator:** Stakeholders left in the dark during recovery

**Remediation Steps:**
1. Define communication cadence during recovery (hourly, every 4 hours, daily)
2. Create status update template
3. Identify stakeholders for recovery communications
4. Assign communication responsibility
5. Include lessons learned communication post-recovery

**Quick Win:** Create a status update template with: current state, next steps, estimated restoration time.

---

## Prioritization Guidance

For organizations starting from scratch, prioritize remediation in this order:

1. **PR.DS-11** — Backups (ransomware defense)
2. **RS.MA-01** — Incident response plan (ability to respond)
3. **ID.AM-01/02** — Asset inventory (foundational visibility)
4. **GV.RR-01** — Accountability (someone owns security)
5. **PR.AA-01** — Credential management (top attack vector)

**Principle:** Start with what protects you from catastrophic loss (backups, IR), then build visibility (inventory), accountability (governance), and prevention (controls).

---

## Canonical Reference

All subcategory IDs align with:

**NIST Cybersecurity Framework (CSF) 2.0**  
NIST CSWP 29, February 26, 2024  
https://doi.org/10.6028/NIST.CSWP.29

---
