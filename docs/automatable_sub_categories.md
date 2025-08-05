# CSF-Lite: Automatable CSF Subcategories

This document lists the subset of CSF-Lite subcategories from the Top 25 that can be either **fully** or **partially automated** using vulnerability scanning tools such as Nuclei. These should form the core of your automated scan logic.

Each entry includes the CSF ID, Function, automation coverage level, and a short description of how it can be addressed via scanning.

---

## 🟦 Identify

### ID.AM-02 — Devices and systems inventoried *(Partial)*

> Nuclei and network scans detect open ports and exposed services, but don’t inventory internal/cloud assets fully.

### ID.RA-05 — External information systems are cataloged *(Partial)*

> Detects exposed API endpoints, public tokens, and leaked credentials, but not vendor lists or formal tracking.

---

## 🟩 Protect

### PR.AC-01 — Identities and credentials are managed *(Full)*

> Nuclei checks like `default-logins/*` detect default or weak credentials on exposed services.

### PR.AC-03 — Remote access is managed *(Full)*

> Templates such as `auth/open-admin` detect admin panels or management interfaces lacking authentication.

### PR.DS-01 — Data-at-rest is protected *(Full)*

> Missing HTTP headers like `X-Content-Type-Options` can be identified by header-based Nuclei templates.

### PR.DS-06 — Integrity checking mechanisms are used *(Full)*

> Directory listing, file exposure, or checksum failures are discoverable through Nuclei misconfiguration templates.

### PR.PT-04 — Communications and control networks are protected *(Full)*

> Weak SSL ciphers, self-signed certs, and Heartbleed can be detected via `ssl/*` templates.

---

## 🟨 Detect

### DE.CM-01 — Unauthorized connections and devices are monitored *(Partial)*

> Anomalies like unexpected HTTP 5xx errors can hint at unauthorized behavior but deeper monitoring requires agents.

### DE.CM-07 — Unauthorized changes to systems are monitored *(Partial)*

> Can catch some file exposure/configuration drift, but lacks deep OS-level file integrity monitoring.

### DE.CM-08 — Vulnerability scans are performed *(Full)*

> Nuclei CVE and software template packs perform surface-level vuln scanning.

### DE.AE-01 — Network baselines are established and managed *(Partial)*

> Repeated scanning can reveal changes or anomalies over time, but true baselining requires behavioral analytics.

---

Use these subcategories to guide your scan pack selection, Nuclei template curation, and automation roadmap. Combine with manual checks to achieve full CSF-Lite coverage.
