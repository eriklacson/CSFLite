# CSFLite: Nuclei-to-CSF Mapping (with Remediation)

This table maps Nuclei template categories to NIST CSF v2.0 subcategories used in CSFLite. Includes rationale for each mapping and practical remediation advice.

All subcategory IDs are validated against NIST CSWP 29 (CSF 2.0, February 2024).

---

## Mapping Table

| Template ID Pattern | Finding Name | CSF Function | Subcategory ID | Subcategory Name | Rationale | Suggested Remediation |
|---------------------|--------------|--------------|----------------|------------------|-----------|----------------------|
| `networking/open-ports` | Open Ports Detected | Identify | ID.AM-02 | Inventories of software and systems are maintained | Open ports reveal active services requiring inventory and assessment | Close unnecessary ports or restrict access via firewall/security group |
| `exposures/git-auth-token` | Publicly Exposed Git Auth Token | Identify | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Leaked credentials are critical vulnerabilities | Revoke token immediately, rotate credentials, update .gitignore |
| `exposures/aws-credentials` | Exposed AWS Credentials | Identify | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Cloud credential exposure enables account takeover | Revoke credentials, rotate all keys, audit CloudTrail |
| `exposures/env-file` | Exposed Environment File | Identify | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Env files contain secrets and configuration | Remove public access, rotate all exposed credentials |
| `default-logins/ssh-default-creds` | SSH Default Credentials | Protect | PR.AA-01 | Identities and credentials are managed | Default credentials indicate failed IAM controls | Change default passwords, enforce key-based authentication |
| `default-logins/*` | Default Credentials (various) | Protect | PR.AA-01 | Identities and credentials are managed | Any default credential is an access control failure | Change all default credentials before deployment |
| `auth/open-admin` | Unauthenticated Admin Panel | Protect | PR.AA-03 | Users and services are authenticated | Missing authentication on admin interfaces | Restrict access with authentication, IP allowlists, or VPN |
| `network/ftp-anonymous` | Anonymous FTP Access | Protect | PR.AA-03 | Users and services are authenticated | Anonymous access bypasses authentication | Disable anonymous FTP, require authentication |
| `headers/missing-content-type` | Missing X-Content-Type-Options | Protect | PR.DS-02 | Data-in-transit is protected | Missing security headers enable attacks | Add `X-Content-Type-Options: nosniff` header |
| `headers/missing-hsts` | Missing HSTS Header | Protect | PR.DS-02 | Data-in-transit is protected | Without HSTS, downgrade attacks possible | Add Strict-Transport-Security header |
| `headers/missing-csp` | Missing Content-Security-Policy | Protect | PR.DS-02 | Data-in-transit is protected | Missing CSP increases XSS risk | Implement appropriate CSP header |
| `misconfiguration/dir-listing` | Open Directory Listing | Protect | PR.DS-01 | Data-at-rest is protected | Directory listing exposes file structure | Disable directory listing in web server |
| `misconfiguration/cors-misconfig` | CORS Misconfiguration | Protect | PR.DS-02 | Data-in-transit is protected | Overly permissive CORS enables unauthorized access | Restrict Access-Control-Allow-Origin |
| `ssl/self-signed` | Self-Signed SSL Certificate | Protect | PR.DS-02 | Data-in-transit is protected | Self-signed certs break trust chains | Replace with CA-signed certificate |
| `ssl/expired-cert` | Expired SSL Certificate | Protect | PR.DS-02 | Data-in-transit is protected | Expired certs cause trust warnings | Renew certificate, implement monitoring |
| `ssl/weak-cipher` | Weak SSL/TLS Cipher | Protect | PR.DS-02 | Data-in-transit is protected | Weak ciphers can be broken | Configure strong cipher suites only |
| `network/ssh-weak-algo` | SSH Weak Algorithm | Protect | PR.DS-02 | Data-in-transit is protected | Weak SSH algorithms can be compromised | Configure strong key exchange algorithms |
| `technologies/outdated-*` | Outdated Software Detected | Identify | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Outdated software contains known vulnerabilities | Update to latest secure version |
| `cves/*` | CVE Vulnerability Detected | Identify | ID.RA-01 | Vulnerabilities in assets are identified and recorded | Known CVEs are documented vulnerabilities | Apply vendor patches or mitigations |

---

## CSF Function Distribution

| CSF Function | Template Categories | Count |
|--------------|---------------------|-------|
| **Identify** | exposures/, technologies/, cves/ | 9 |
| **Protect** | default-logins/, auth/, headers/, misconfiguration/, ssl/, network/ | 11 |
| **Detect** | (none directly — scanning IS detection) | 0 |
| **Respond** | (not applicable to scanning) | 0 |
| **Recover** | (not applicable to scanning) | 0 |

**Note:** Nuclei scanning itself is an implementation of detection capabilities (DE.CM-09), but individual findings map to IDENTIFY and PROTECT outcomes.

---

## Severity-to-Priority Mapping

CSFLite uses this mapping for heatmap scoring:

| Nuclei Severity | Base Score | Rationale |
|-----------------|------------|-----------|
| critical | 4 | Immediate exploitation risk |
| high | 3 | Significant risk, prioritize remediation |
| medium | 2 | Moderate risk, schedule remediation |
| low | 1 | Minor risk, address in routine maintenance |
| info | 0 | Informational, no inherent risk |

**Weighted Score Formula:**  
`weighted_score = subcategory_weight × (severity_score + ln(1 + finding_count))`

---

## Template Selection for CSFLite

Recommended Nuclei template directories for CSFLite assessments:

### Tier 1 — Critical (Always Run)
```
nuclei -t cves/ -t default-logins/ -t exposures/ -severity critical,high
```

### Tier 2 — Standard Assessment
```
nuclei -t ssl/ -t headers/ -t misconfiguration/ -t technologies/ -severity medium,high,critical
```

### Tier 3 — Comprehensive
```
nuclei -t network/ -t auth/ -severity low,medium,high,critical
```

---

## Unmapped Findings

Some Nuclei findings don't map cleanly to CSFLite Top 25. Handle as follows:

| Finding Type | Recommended Mapping | Notes |
|--------------|---------------------|-------|
| Information disclosure | ID.RA-01 | Treat as vulnerability |
| WAF bypass | PR.IR-01 | Network protection gap |
| Rate limiting issues | PR.IR-01 | Availability protection |
| API security issues | PR.AA-03 or PR.DS-02 | Authentication or transport |

---

## Canonical Reference

All subcategory IDs validated against:

**NIST Cybersecurity Framework (CSF) 2.0**  
NIST CSWP 29, February 26, 2024  
https://doi.org/10.6028/NIST.CSWP.29

---
