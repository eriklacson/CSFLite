# CSF-Lite: Automatable CSF Subcategories

This document lists the subset of CSF-Lite subcategories from the Top 25 that can be either **fully** or **partially automated** using vulnerability scanning tools such as Nuclei. These should form the core of your automated scan logic.

Each entry includes the CSF ID, Function, automation coverage level, and a short description of how it can be addressed via scanning.

---

## Identify

### ID.AM-02 — Assets and systems are inventoried *(Partial)*
> Nuclei scans detect open ports and exposed services, but not inventory internal/cloud assets fully.

### ### ID.AM-03 — Baseline of operations/data flows established & managed *(Partial)*
> Repeated scanning can detect changes in expected service behaviors, but full baselining still requires operational analytics.

### ID.AM-04 — External information systems are cataloged *(Partial)*
> Discovery scans can highlight poentenial vulnerabilities in third-party services, but contracts and ownership must be validated manually.

### ID.RA-01 — Vulnerability scans are performed *(Full)*
> Nuclei CVE and software templates can deliver actionable vulnerability data. CSFLite toolkits are available to map the results to framework sub-categories

---

## Protect

### PR.AA-01 — Identities and credentials are managed *(Partial)*

> Nuclei checks like `default-logins/*` detect default or weak credentials on exposed services, but IAM governance is done manually.

### PR.AA-03 — Users/services/hardware are authenticated *(Partial)*
> Templates such as `auth/open-admin` detect admin panels lacking authentication. Granular access control reviews require manual review.

### PR.DS-01 — Data-at-rest is protected *(Partial)*
> Missing HTTP security headers and exposed storage services can be detected, but encryption enforcement must be verified through configuration review.

## PR.DS-10 — Integrity checking mechanisms are used *(Partial)*
> Results from directory listing or file exposure scans indicate weak integrity controls. Comprehensive integrity monitoring needs additional tooling.

### PR.IR-01 — Communications and control networks are protected *(Partial)*
> SSL/TLS misconfiguration templates indicate insecure transport protections. network segmentation validation needs to be conducted manually.


---

## Detect

### DE.CM-01 — The network is monitored to detect potential cybersecurity events *(Partial)*
> Automated scans can surface indicators of compromise, but real-time monitoring and alerting depend on SOC processes.

### DE.CM-07 — Unauthorized changes to systems are monitored *(Partial)*

> > Scans can flag unexpected content or configuration drift, while full change detection requires dedicated monitoring platforms.

---

Use these subcategories to guide your scan pack selection, Nuclei template curation, and automation roadmap. Combine with manual checks to achieve full CSFLite coverage.
