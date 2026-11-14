# CSFLite to CIS IG1 — Control Crosswalk

Maps all 25 CSFLite controls to their primary CIS IG1 counterparts.

## How to Read This Crosswalk

Each CSFLite control (a curated NIST CSF 2.0 subcategory) maps to one or more controls. The assessment method column describes how an assessor evaluates the control using three methods:

| Method | Description |
|---|---|
| **Examine** | Review documents, records, configurations, and artifacts to confirm the control is documented and configured |
| **Interview** | Discuss with responsible personnel to verify understanding, awareness, and operational execution |
| **Test** | Directly observe or exercise the control to verify it operates as described |

Some CIS IG1 controls appear under multiple CSFLite entries. In an SSP, each CIS IG1 control is documented once with a single implementation narrative, even if it satisfies multiple CSF subcategories.

CSFLite measures control coverage (Yes / Partial / No). CIS IG1 assessment determines Satisfied / Other Than Satisfied per control objective.

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

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 3.1 | Establish and Maintain a Data Management Process | Establish and maintain a documented data management process. In the process, address data sensitivity, data owner, handling of data, data retention limits, and disposal requirements, based on sensitivity and retention standards for the enterprise. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard.|
| CIS 4.1 | Establish and Maintain a Secure Configuration Process | Establish and maintain a documented secure configuration process for enterprise assets (end-user devices, including portable and mobile, non-computing/IoT devices, and servers) and software (operating systems and applications). Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 7.1 | Establish and Maintain a Vulnerability Management Process | Establish and maintain a documented vulnerability management process for enterprise assets. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 8.1 | Establish and Maintain an Audit Log Management Process | Establish and maintain a documented audit log management process that defines the enterprise’s logging requirements. At a minimum, address the collection, review, and retention of audit logs for enterprise assets. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 11.1 | Establish and Maintain a Data Recovery Process | Establish and maintain a documented data recovery process. In the process, address the scope of data recovery activities, recovery prioritization, and the security of backup data. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 14.1 | Establish and Maintain a Security Awareness Program | Establish and maintain a security awareness program. The purpose of a security awareness program is to educate the enterprise's workforce on how to interact with enterprise assets and data in a secure manner. Conduct training at hire and, at a minimum, annually. Review and update content annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 14.2 | Train Workforce Members to Recognize Social Engineering Attacks | Train workforce members to recognize social engineering attacks, such as phishing, business email compromise (BEC), pretexting, and tailgating. |
| CIS 14.3 | Train Workforce Members on Authentication Best Practices | Train workforce members on authentication best practices. Example topics include MFA, password composition, and credential management. |
| CIS 14.4 | Train Workforce on Data Handling Best Practices | Train workforce members on how to identify and properly store, transfer, archive, and destroy sensitive data. This also includes training workforce members on clear screen and desk best practices, such as locking their screen when they step away from their enterprise asset, erasing physical and virtual whiteboards at the end of meetings, and storing data and assets securely. |
| CIS 14.5 | Train Workforce Members on Causes of Unintentional Data Exposure | Train workforce members to be aware of causes for unintentional data exposure. Example topics include mis-delivery of sensitive data, losing a portable end-user device, or publishing data to unintended audiences. |
| CIS 14.6 | Train Workforce Members on Recognizing and Reporting Security Incidents | Train workforce members to be able to recognize a potential incident and be able to report such an incident. |
| CIS 14.7 | Train Workforce on How to Identify and Report if Their Enterprise Assets are Missing Security Updates | Train workforce to understand how to verify and report out-of-date software patches or any failures in automated processes and tools. Part of this training should include notifying IT personnel of any failures in automated processes and tools. |
| CIS 14.8 | Train Workforce on the Dangers of Connecting to and Transmitting Enterprise Data Over Insecure Networks | Train workforce members on the dangers of connecting to, and transmitting data over, insecure networks for enterprise activities. If the enterprise has remote workers, training must include guidance to ensure that all users securely configure their home network infrastructure. |
| ACP | Access Control Policy | foundational administrative and technical control that defines the rules, rights, and restrictions governing user identities, authentication mechanisms, and authorization levels across an organization's systems and data. |
| AUP | Acceptable Use Policy | Outlines explicit rules, boundaries, and behavioral expectations for employees regarding the use of corporate IT assets, network resources, internet access, and email systems. It establishes clear security practices to mitigate human error, limits unauthorized third-party software (Shadow IT), and defines acceptable boundaries for modern technology usage, such as generative Artificial Intelligence (AI) tools. |
| BDP | Data Backup and Retention Policy | Establishes mandatory procedures, frequencies, and retention rules for creating, protecting, and restoring organizational data backups. It mandates automated schedules, offsite storage, and immutable backups. |
| GCP | General Cibersecurity Policy |  Establishes the formal rules, expectations, and behavioral guidelines for an organization's members. It defines what is permissible and prohibited regarding information assets, setting the baseline for legal compliance, accountability, and organizational risk management. |
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |

### GV.RR-01 — Organizational leadership is responsible and accountable for cybersecurity risk

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 14.1 | Establish and Maintain a Security Awareness Program | Establish and maintain a security awareness program. The purpose of a security awareness program is to educate the enterprise's workforce on how to interact with enterprise assets and data in a secure manner. Conduct training at hire and, at a minimum, annually. Review and update content annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 17.1 | Designate Personnel to Manage Incident Handling | Designate one key person, and at least one backup, who will manage the enterprise’s incident handling process. Management personnel are responsible for the coordination and documentation of incident response and recovery efforts and can consist of employees internal to the enterprise, service providers, or a hybrid approach. If using a service provider, designate at least one person internal to the enterprise to oversee any third-party work. Review annually, or when significant enterprise changes occur that could impact this Safeguard. |
| AUP | Acceptable Use Policy | Outlines explicit rules, boundaries, and behavioral expectations for employees regarding the use of corporate IT assets, network resources, internet access, and email systems. It establishes clear security practices to mitigate human error, limits unauthorized third-party software (Shadow IT), and defines acceptable boundaries for modern technology usage, such as generative Artificial Intelligence (AI) tools. |
| GCP  | General Cibersecurity Policy |  Establishes the formal rules, expectations, and behavioral guidelines for an organization's members. It defines what is permissible and prohibited regarding information assets, setting the baseline for legal compliance, accountability, and organizational risk management. |
| RACI  | Responsibility matrix | Defines, assigns, and clarifies roles and responsibilities across organizational processes and projects. |

### GV.RM-01 — Risk management objectives are established and agreed to by organizational stakeholders

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| BIA | Business Impact Analysis | Foundational risk assessment and operational governance control that evaluates the potential consequences of a disruption to an organization's core business processes. It identifies mission-critical functions, quantifies operational and financial losses over time, and establishes essential recovery metrics—such as the Recovery Time Objective (RTO) and Recovery Point Objective (RPO). |
| GCP  | General Cibersecurity Policy |  Establishes the formal rules, expectations, and behavioral guidelines for an organization's members. It defines what is permissible and prohibited regarding information assets, setting the baseline for legal compliance, accountability, and organizational risk management. |
| RACI  | Responsibility matrix | Defines, assigns, and clarifies roles and responsibilities across organizational processes and projects. |

### GV.SC-01 — A cybersecurity supply chain risk management program is established

**Weight:** 1.0

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 15.1 | Establish and Maintain an Inventory of Service Providers | Establish and maintain an inventory of service providers. The inventory is to list all known service providers, include classification(s), and designate an enterprise contact for each service provider. Review and update the inventory annually, or when significant enterprise changes occur that could impact this Safeguard. |
| GCP  | General Cibersecurity Policy |  Establishes the formal rules, expectations, and behavioral guidelines for an organization's members. It defines what is permissible and prohibited regarding information assets, setting the baseline for legal compliance, accountability, and organizational risk management. |
| RACI  | Responsibility matrix | Defines, assigns, and clarifies roles and responsibilities across organizational processes and projects. |

---

## IDENTIFY

### ID.AM-01 — Inventories of hardware managed by the organization are maintained

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 1.1 | Establish and Maintain Detailed Enterprise Asset Inventory | Establish and maintain an accurate, detailed, and up-to-date inventory of all enterprise assets with the potential to store or process data, to include: end-user devices (including portable and mobile), network devices, non-computing/IoT devices, and servers. Ensure the inventory records the network address (if static), hardware address, machine name, enterprise asset owner, department for each asset, and whether the asset has been approved to connect to the network. For mobile end-user devices, MDM type tools can support this process, where appropriate. This inventory includes assets connected to the infrastructure physically, virtually, remotely, and those within cloud environments. Additionally, it includes assets that are regularly connected to the enterprise’s network infrastructure, even if they are not under control of the enterprise. Review and update the inventory of all enterprise assets bi-annually, or more frequently. |
| CIS 1.2 | Address Unauthorized Assets | Ensure that a process exists to address unauthorized assets on a weekly basis. The enterprise may choose to remove the asset from the network, deny the asset from connecting remotely to the network, or quarantine the asset. |

### ID.AM-02 — Inventories of software and systems managed by the organization are maintained

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 2.1 | Establish and Maintain a Software Inventory | Establish and maintain a detailed inventory of all licensed software installed on enterprise assets. The software inventory must document the title, publisher, initial install/use date, and business purpose for each entry; where appropriate, include the Uniform Resource Locator (URL), app store(s), version(s), deployment mechanism, decommission date, and number of licenses. Review and update the software inventory bi-annually, or more frequently. |
| CIS 2.2 | Ensure Authorized Software is Currently Supported | Ensure that only currently supported software is designated as authorized in the software inventory for enterprise assets. If software is unsupported, yet necessary for the fulfillment of the enterprise’s mission, document an exception detailing mitigating controls and residual risk acceptance. For any unsupported software without an exception documentation, designate as unauthorized. Review the software list to verify software support at least monthly, or more frequently. |
| CIS 2.3 | Address Unauthorized Software | Ensure that unauthorized software is either removed from use on enterprise assets or receives a documented exception. Review monthly, or more frequently. |
| AUP | Acceptable Use Policy | Outlines explicit rules, boundaries, and behavioral expectations for employees regarding the use of corporate IT assets, network resources, internet access, and email systems. It establishes clear security practices to mitigate human error, limits unauthorized third-party software (Shadow IT), and defines acceptable boundaries for modern technology usage, such as generative Artificial Intelligence (AI) tools. |

### ID.AM-05 — Assets are prioritized based on classification and criticality

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 1.1 | Establish and Maintain Detailed Enterprise Asset Inventory | Establish and maintain an accurate, detailed, and up-to-date inventory of all enterprise assets with the potential to store or process data, to include: end-user devices (including portable and mobile), network devices, non-computing/IoT devices, and servers. Ensure the inventory records the network address (if static), hardware address, machine name, enterprise asset owner, department for each asset, and whether the asset has been approved to connect to the network. For mobile end-user devices, MDM type tools can support this process, where appropriate. This inventory includes assets connected to the infrastructure physically, virtually, remotely, and those within cloud environments. Additionally, it includes assets that are regularly connected to the enterprise’s network infrastructure, even if they are not under control of the enterprise. Review and update the inventory of all enterprise assets bi-annually, or more frequently. |
| CIS 2.1 | Establish and Maintain a Software Inventory | Establish and maintain a detailed inventory of all licensed software installed on enterprise assets. The software inventory must document the title, publisher, initial install/use date, and business purpose for each entry; where appropriate, include the Uniform Resource Locator (URL), app store(s), version(s), deployment mechanism, decommission date, and number of licenses. Review and update the software inventory bi-annually, or more frequently. |
| CIS 3.1 | Establish and Maintain a Data Management Process | Establish and maintain a documented data management process. In the process, address data sensitivity, data owner, handling of data, data retention limits, and disposal requirements, based on sensitivity and retention standards for the enterprise. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| BDP | Data Backup and Retention Policy | Establishes mandatory procedures, frequencies, and retention rules for creating, protecting, and restoring organizational data backups. It mandates automated schedules, offsite storage, and immutable backups. |
| BIA | Business Impact Analysis | Foundational risk assessment and operational governance control that evaluates the potential consequences of a disruption to an organization's core business processes. It identifies mission-critical functions, quantifies operational and financial losses over time, and establishes essential recovery metrics—such as the Recovery Time Objective (RTO) and Recovery Point Objective (RPO). |


### ID.RA-01 — Vulnerabilities in assets are identified and recorded

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 7.1 | Establish and Maintain a Vulnerability Management Process | Establish and maintain a documented vulnerability management process for enterprise assets. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 7.2 | Establish and Maintain a Remediation Process | Establish and maintain a risk-based remediation strategy documented in a remediation process, with monthly, or more frequent, reviews. |

### ID.RA-05 — Threats and vulnerabilities are used to understand inherent risk and prioritize response

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 7.1 | Establish and Maintain a Vulnerability Management Process | Establish and maintain a documented vulnerability management process for enterprise assets. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 7.2 | Establish and Maintain a Remediation Process | Establish and maintain a risk-based remediation strategy documented in a remediation process, with monthly, or more frequent, reviews. |
| GCP  | General Cibersecurity Policy |  Establishes the formal rules, expectations, and behavioral guidelines for an organization's members. It defines what is permissible and prohibited regarding information assets, setting the baseline for legal compliance, accountability, and organizational risk management. |

---

## PROTECT

### PR.AA-01 — Identities and credentials for authorized users and services are managed

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 4.7 | Manage Default Accounts on Enterprise Assets and Software | Manage default accounts on enterprise assets and software, such as root, administrator, and other pre-configured vendor accounts. Example implementations can include: disabling default accounts or making them unusable. |
| CIS 5.1 | Establish and Maintain an Inventory of Accounts | Establish and maintain an inventory of all accounts managed in the enterprise. The inventory must at a minimum include user, administrator accounts, and service accounts. The inventory, at a minimum, should contain the person’s name, username, start/stop dates, and department. Validate that all active accounts are authorized, on a recurring schedule at a minimum quarterly, or more frequently. |
| CIS 5.2 | Use Unique Passwords | Use unique passwords for all enterprise assets. Best practice implementation includes, at a minimum, an 8-character password for accounts using Multi-Factor Authentication (MFA) and a 14-character password for accounts not using MFA. |
| CIS 5.3 | Disable Dormant Accounts | Delete or disable any dormant accounts after a period of 45 days of inactivity, where supported. |
| CIS 5.4 | Restrict Administrator Privileges to Dedicated Administrator Accounts | Restrict administrator privileges to dedicated administrator accounts on enterprise assets. Conduct general computing activities, such as internet browsing, email, and productivity suite use, from the user’s primary, non-privileged account. |
| CIS 6.1 | Establish an Access Granting Process | Establish and follow a documented process, preferably automated, for granting access to enterprise assets upon new hire or role change of a user. |
| CIS 6.2 | Establish an Access Revoking Process | Establish and follow a process, preferably automated, for revoking access to enterprise assets, through disabling accounts immediately upon termination, rights revocation, or role change of a user. Disabling accounts, instead of deleting accounts, may be necessary to preserve audit trails. |
| ACP | Access Control Policy | foundational administrative and technical control that defines the rules, rights, and restrictions governing user identities, authentication mechanisms, and authorization levels across an organization's systems and data. |

### PR.AA-03 — Users and services are authenticated

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 5.2 | Use Unique Passwords | Use unique passwords for all enterprise assets. Best practice implementation includes, at a minimum, an 8-character password for accounts using Multi-Factor Authentication (MFA) and a 14-character password for accounts not using MFA. |
| CIS 6.3 | Multi-Factor Authentication to Privileged Accounts | Test: verify MFA on all admin accounts. Examine: MFA policy scope. |
| CIS 6.4 | Require MFA for Remote Network Access | Require MFA for remote network access. |
| CIS 6.5 | Require MFA for Administrative Access | Require MFA for all administrative access accounts, where supported, on all enterprise assets, whether managed on-site or through a service provider. |
| CIS 14.3 | Train Workforce Members on Authentication Best Practices | Train workforce members on authentication best practices. Example topics include MFA, password composition, and credential management. |
| ACP | Access Control Policy | foundational administrative and technical control that defines the rules, rights, and restrictions governing user identities, authentication mechanisms, and authorization levels across an organization's systems and data. |
| AUP | Acceptable Use Policy | Outlines explicit rules, boundaries, and behavioral expectations for employees regarding the use of corporate IT assets, network resources, internet access, and email systems. It establishes clear security practices to mitigate human error, limits unauthorized third-party software (Shadow IT), and defines acceptable boundaries for modern technology usage, such as generative Artificial Intelligence (AI) tools. |

### PR.DS-01 — The confidentiality and integrity of data-at-rest are protected

**Weight:** 1.0

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 3.1 | Establish and Maintain a Data Management Process | Establish and maintain a documented data management process. In the process, address data sensitivity, data owner, handling of data, data retention limits, and disposal requirements, based on sensitivity and retention standards for the enterprise. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 3.2 | Establish and Maintain a Data Inventory | Establish and maintain a data inventory based on the enterprise’s data management process. Inventory sensitive data, at a minimum. Review and update inventory annually, at a minimum, with a priority on sensitive data. |
| CIS 3.3 | Configure Data Access Control Lists | Configure data access control lists based on a user’s need to know. Apply data access control lists, also known as access permissions, to local and remote file systems, databases, and applications. |
| CIS 3.4 | Enforce Data Retention | Retain data according to the enterprise’s documented data management process. Data retention must include both minimum and maximum timelines. |
| CIS 3.5 | Securely Dispose of Data | Securely dispose of data as outlined in the enterprise’s documented data management process. Ensure the disposal process and method are commensurate with the data sensitivity. |
| CIS 3.6 | Encrypt Data on End-User Devices | Encrypt data on end-user devices containing sensitive data. Example implementations can include: Windows BitLocker®, Apple FileVault®, Linux® dm-crypt. |
| ACP | Access Control Policy | foundational administrative and technical control that defines the rules, rights, and restrictions governing user identities, authentication mechanisms, and authorization levels across an organization's systems and data. |
| AUP | Acceptable Use Policy | Outlines explicit rules, boundaries, and behavioral expectations for employees regarding the use of corporate IT assets, network resources, internet access, and email systems. It establishes clear security practices to mitigate human error, limits unauthorized third-party software (Shadow IT), and defines acceptable boundaries for modern technology usage, such as generative Artificial Intelligence (AI) tools. |

### PR.DS-02 — The confidentiality and integrity of data-in-transit are protected

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 14.8 | Train Workforce on the Dangers of Connecting to and Transmitting Enterprise Data Over Insecure Networks | Train workforce members on the dangers of connecting to, and transmitting data over, insecure networks for enterprise activities. If the enterprise has remote workers, training must include guidance to ensure that all users securely configure their home network infrastructure. |
| AUP | Acceptable Use Policy | Outlines explicit rules, boundaries, and behavioral expectations for employees regarding the use of corporate IT assets, network resources, internet access, and email systems. It establishes clear security practices to mitigate human error, limits unauthorized third-party software (Shadow IT), and defines acceptable boundaries for modern technology usage, such as generative Artificial Intelligence (AI) tools. |
| GCP  | General Cibersecurity Policy |  Establishes the formal rules, expectations, and behavioral guidelines for an organization's members. It defines what is permissible and prohibited regarding information assets, setting the baseline for legal compliance, accountability, and organizational risk management. |

### PR.DS-11 — Backups of data are created and tested

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 3.1 | Establish and Maintain a Data Management Process | Establish and maintain a documented data management process. In the process, address data sensitivity, data owner, handling of data, data retention limits, and disposal requirements, based on sensitivity and retention standards for the enterprise. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 11.1 | Establish and Maintain a Data Recovery Process | Establish and maintain a documented data recovery process. In the process, address the scope of data recovery activities, recovery prioritization, and the security of backup data. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 11.2 | Perform Automated Backups | Perform automated backups of in-scope enterprise assets. Run backups weekly, or more frequently, based on the sensitivity of the data. |
| CIS 11.3 | Protect Recovery Data | Protect recovery data with equivalent controls to the original data. Reference encryption or data separation, based on requirements. |
| CIS 11.4 | Establish and Maintain an Isolated Instance of Recovery Data | Establish and maintain an isolated instance of recovery data. Example implementations include, version controlling backup destinations through offline, cloud, or off-site systems or services. |
| BIA | Business Impact Analysis | Foundational risk assessment and operational governance control that evaluates the potential consequences of a disruption to an organization's core business processes. It identifies mission-critical functions, quantifies operational and financial losses over time, and establishes essential recovery metrics—such as the Recovery Time Objective (RTO) and Recovery Point Objective (RPO). |
| BDP | Data Backup and Retention Policy | Establishes mandatory procedures, frequencies, and retention rules for creating, protecting, and restoring organizational data backups. It mandates automated schedules, offsite storage, and immutable backups. |
| GCP  | General Cibersecurity Policy |  Establishes the formal rules, expectations, and behavioral guidelines for an organization's members. It defines what is permissible and prohibited regarding information assets, setting the baseline for legal compliance, accountability, and organizational risk management. |
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |

### PR.IR-01 — Networks and environments are protected from unauthorized logical access

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 4.1 | Establish and Maintain a Secure Configuration Process | Establish and maintain a documented secure configuration process for enterprise assets (end-user devices, including portable and mobile, non-computing/IoT devices, and servers) and software (operating systems and applications). Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 4.2 | Establish and Maintain a Secure Configuration Process for Network Infrastructure | Establish and maintain a documented secure configuration process for network devices. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 4.3 | Configure Automatic Session Locking on Enterprise Assets | Configure automatic session locking on enterprise assets after a defined period of inactivity. For general purpose operating systems, the period must not exceed 15 minutes. For mobile end-user devices, the period must not exceed 2 minutes. |
| CIS 4.4 | Implement and Manage a Firewall on Servers | Implement and manage a firewall on servers, where supported. Example implementations include a virtual firewall, operating system firewall, or a third-party firewall agent. |
| CIS 4.5 | Implement and Manage a Firewall on End-User Devices | Implement and manage a host-based firewall or port-filtering tool on end-user devices, with a default-deny rule that drops all traffic except those services and ports that are explicitly allowed. |
| CIS 4.6 | Securely Manage Enterprise Assets and Software | Securely manage enterprise assets and software. Example implementations include managing configuration through version-controlled Infrastructure-as-Code (IaC) and accessing administrative interfaces over secure network protocols, such as Secure Shell (SSH) and Hypertext Transfer Protocol Secure (HTTPS). Do not use insecure management protocols, such as Telnet (Teletype Network) and HTTP, unless operationally essential. |
| CIS 6.4 | Require MFA for Remote Network Access | Require MFA for remote network access. |
| CIS 7.3 | Perform Automated Operating System Patch Management | Perform operating system updates on enterprise assets through automated patch management on a monthly, or more frequent, basis. |
| CIS 7.4 | Perform Automated Application Patch Management | Perform application updates on enterprise assets through automated patch management on a monthly, or more frequent, basis. |
| CIS 9.1 | Ensure Use of Only Fully Supported Browsers and Email Clients | Ensure only fully supported browsers and email clients are allowed to execute in the enterprise, only using the latest version of browsers and email clients provided through the vendor. |
| CIS 9.2 | Use DNS Filtering Services | Use DNS filtering services on all end-user devices, including remote and on-premises assets, to block access to known malicious domains. |
| CIS 10.1 | Deploy and Maintain Anti-Malware Software | Deploy and maintain anti-malware software on all enterprise assets. |
| CIS 10.2 | Configure Automatic Anti-Malware Signature Updates | Configure automatic updates for anti-malware signature files on all enterprise assets. |
| CIS 10.3 | Disable Autorun and Autoplay for Removable Media | Disable autorun and autoplay auto-execute functionality for removable media. |
| CIS 12.1 | Ensure Network Infrastructure is Up-to-Date | Ensure network infrastructure is kept up-to-date. Example implementations include running the latest stable release of software and/or using currently supported network-as-a-service (NaaS) offerings. Review software versions monthly, or more frequently, to verify software support. |
| ACP | Access Control Policy | foundational administrative and technical control that defines the rules, rights, and restrictions governing user identities, authentication mechanisms, and authorization levels across an organization's systems and data. |
| AUP | Acceptable Use Policy | Outlines explicit rules, boundaries, and behavioral expectations for employees regarding the use of corporate IT assets, network resources, internet access, and email systems. It establishes clear security practices to mitigate human error, limits unauthorized third-party software (Shadow IT), and defines acceptable boundaries for modern technology usage, such as generative Artificial Intelligence (AI) tools. |

---

## DETECT

### DE.CM-01 — Networks and network services are monitored to find potentially adverse events

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 8.1 | Establish and Maintain an Audit Log Management Process | Establish and maintain a documented audit log management process that defines the enterprise’s logging requirements. At a minimum, address the collection, review, and retention of audit logs for enterprise assets. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 8.2 | Collect Audit Logs | Collect audit logs. Ensure that logging, per the enterprise’s audit log management process, has been enabled across enterprise assets. |
| CIS 8.3 | Ensure Adequate Audit Log Storage | Ensure that logging destinations maintain adequate storage to comply with the enterprise’s audit log management process. |

### DE.CM-09 — Computing hardware and software are monitored to find potentially adverse events

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 8.1 | Establish and Maintain an Audit Log Management Process | Establish and maintain a documented audit log management process that defines the enterprise’s logging requirements. At a minimum, address the collection, review, and retention of audit logs for enterprise assets. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 8.2 | Collect Audit Logs | Collect audit logs. Ensure that logging, per the enterprise’s audit log management process, has been enabled across enterprise assets. |
| CIS 8.3 | Ensure Adequate Audit Log Storage | Ensure that logging destinations maintain adequate storage to comply with the enterprise’s audit log management process. |
| CIS 10.1 | Deploy and Maintain Anti-Malware Software | Deploy and maintain anti-malware software on all enterprise assets. |
| CIS 10.2 | Configure Automatic Anti-Malware Signature Updates | Configure automatic updates for anti-malware signature files on all enterprise assets. |

### DE.AE-02 — Potentially adverse events are analyzed to understand associated activities

**Weight:** 1.0

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 8.2 | Collect Audit Logs | Collect audit logs. Ensure that logging, per the enterprise’s audit log management process, has been enabled across enterprise assets. |

### DE.AE-08 — Incidents are declared when adverse events meet defined incident criteria

**Weight:** 1.0

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 17.1 | Designate Personnel to Manage Incident Handling | Designate one key person, and at least one backup, who will manage the enterprise’s incident handling process. Management personnel are responsible for the coordination and documentation of incident response and recovery efforts and can consist of employees internal to the enterprise, service providers, or a hybrid approach. If using a service provider, designate at least one person internal to the enterprise to oversee any third-party work. Review annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 17.2 | Establish and Maintain Contact Information for Reporting Security Incidents | Establish and maintain contact information for parties that need to be informed of security incidents. Contacts may include internal staff, service vendors, law enforcement, cyber insurance providers, relevant government agencies, Information Sharing and Analysis Center (ISAC) partners, or other stakeholders. Verify contacts annually to ensure that information is up-to-date. |
| CIS 17.3 | Establish and Maintain an Enterprise Process for Reporting Incidents | Establish and maintain an documented enterprise process for the workforce to report security incidents. The process includes reporting timeframe, personnel to report to, mechanism for reporting, and the minimum information to be reported. Ensure the process is publicly available to all of the workforce. Review annually, or when significant enterprise changes occur that could impact this Safeguard. |
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |


---

## RESPOND

### RS.MA-01 — The incident response plan is executed in coordination with relevant third parties

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 17.1 | Designate Personnel to Manage Incident Handling | Designate one key person, and at least one backup, who will manage the enterprise’s incident handling process. Management personnel are responsible for the coordination and documentation of incident response and recovery efforts and can consist of employees internal to the enterprise, service providers, or a hybrid approach. If using a service provider, designate at least one person internal to the enterprise to oversee any third-party work. Review annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 17.2 | Establish and Maintain Contact Information for Reporting Security Incidents | Establish and maintain contact information for parties that need to be informed of security incidents. Contacts may include internal staff, service vendors, law enforcement, cyber insurance providers, relevant government agencies, Information Sharing and Analysis Center (ISAC) partners, or other stakeholders. Verify contacts annually to ensure that information is up-to-date. |
| CIS 17.3 | Establish and Maintain an Enterprise Process for Reporting Incidents | Establish and maintain an documented enterprise process for the workforce to report security incidents. The process includes reporting timeframe, personnel to report to, mechanism for reporting, and the minimum information to be reported. Ensure the process is publicly available to all of the workforce. Review annually, or when significant enterprise changes occur that could impact this Safeguard. |
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |


### RS.CO-02 — Internal and external stakeholders are notified of incidents

**Weight:** 1.0

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 14.6 | Train Workforce Members on Recognizing and Reporting Security Incidents | Train workforce members to be able to recognize a potential incident and be able to report such an incident. |
| CIS 17.2 | Establish and Maintain Contact Information for Reporting Security Incidents | Establish and maintain contact information for parties that need to be informed of security incidents. Contacts may include internal staff, service vendors, law enforcement, cyber insurance providers, relevant government agencies, Information Sharing and Analysis Center (ISAC) partners, or other stakeholders. Verify contacts annually to ensure that information is up-to-date. |
| CIS 17.3 | Establish and Maintain an Enterprise Process for Reporting Incidents | Establish and maintain an documented enterprise process for the workforce to report security incidents. The process includes reporting timeframe, personnel to report to, mechanism for reporting, and the minimum information to be reported. Ensure the process is publicly available to all of the workforce. Review annually, or when significant enterprise changes occur that could impact this Safeguard. |
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |

### RS.MI-01 — Incidents are contained

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| IRP | Incident Respose Playbook           | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |


### RS.MI-02 — Incidents are eradicated

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |


---

## RECOVER

### RC.RP-01 — The recovery portion of the incident response plan is executed

**Weight:** 1.5

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 11.1 | Establish and Maintain a Data Recovery Process | Establish and maintain a documented data recovery process. In the process, address the scope of data recovery activities, recovery prioritization, and the security of backup data. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard. |
| CIS 11.2 | Perform Automated Backups | Perform automated backups of in-scope enterprise assets. Run backups weekly, or more frequently, based on the sensitivity of the data. |
| CIS 11.3 | Protect Recovery Data | Protect recovery data with equivalent controls to the original data. Reference encryption or data separation, based on requirements. |
| CIS 11.4 | Establish and Maintain an Isolated Instance of Recovery Data | Establish and maintain an isolated instance of recovery data. Example implementations include, version controlling backup destinations through offline, cloud, or off-site systems or services. |
| BIA | Business Impact Analysis | Foundational risk assessment and operational governance control that evaluates the potential consequences of a disruption to an organization's core business processes. It identifies mission-critical functions, quantifies operational and financial losses over time, and establishes essential recovery metrics—such as the Recovery Time Objective (RTO) and Recovery Point Objective (RPO). |
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |
| BDP | Data Backup and Retention Policy | Establishes mandatory procedures, frequencies, and retention rules for creating, protecting, and restoring organizational data backups. It mandates automated schedules, offsite storage, and immutable backups. |

### RC.CO-03 — Recovery activities and progress are communicated to stakeholders

**Weight:** 1.2

| Control | Control Name | Assessment Method |
|---|---|---|
| CIS 17.2 | Establish and Maintain Contact Information for Reporting Security Incidents | Establish and maintain contact information for parties that need to be informed of security incidents. Contacts may include internal staff, service vendors, law enforcement, cyber insurance providers, relevant government agencies, Information Sharing and Analysis Center (ISAC) partners, or other stakeholders. Verify contacts annually to ensure that information is up-to-date. |
| IRP | Incident Respose Playbook | Provides a structured, step-by-step workflow for detecting, containing, eradicating, and recovering from cybersecurity incidents. Designed as an actionable, single-page operational guide, it defines emergency contact protocols, internal and external escalation paths. |

---

## References

- CIS IG1
- NIST Cybersecurity Framework 2.0 (CSWP 29)
- CSFLite — github.com/eriklacson/CSFLite

---

*This crosswalk maps to primary CIS IG1 controls. 
