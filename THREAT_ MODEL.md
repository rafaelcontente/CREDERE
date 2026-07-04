

> **Security is not achieved by assuming the system will never be attacked. It is achieved by assuming that attacks will occur and engineering the system to fail safely.**

This document describes the primary security threats considered during the design of CREDERE, their potential impact, and the architectural mechanisms implemented to mitigate them.

The objective is not to claim immunity against attacks, but to demonstrate that security, robustness and trustworthiness were considered as first-class architectural concerns.

---

# Security Philosophy

CREDERE follows four fundamental security principles:

- **Defense in Depth**
- **Least Privilege**
- **Fail Closed**
- **Complete Auditability**

Rather than relying on a single protective mechanism, multiple independent layers reduce the likelihood that a single failure compromises the entire decision process.

---

# Assets to Protect

The primary assets of the system are:

- Credit applications
- Customer information
- Prediction results
- Compliance decisions
- Explanations
- Audit records
- Business rules
- Model integrity
- System availability

---

# Threat Categories

Threats were analysed across the complete decision pipeline.

| Category | Example |
|----------|----------|
| Input Manipulation | Malicious application data |
| Model Abuse | Gaming the scoring model |
| Compliance Bypass | Circumventing deterministic rules |
| Explanation Manipulation | Altering customer explanations |
| Audit Tampering | Modifying historical decisions |
| Insider Threats | Unauthorized rule modification |
| Availability | Denial-of-Service attacks |
| Privacy | Exposure of sensitive information |

---

# System Attack Surface

```
User

↓

Input Validation

↓

Credit Model

↓

Compliance Engine

↓

Explanation Engine

↓

Fact Checker

↓

Audit Ledger

↓

Output
```

Each stage introduces different security considerations.

---

# Threat 1 — Invalid Input Injection

## Description

An attacker submits malformed or unexpected values intended to:

- crash the system;
- bypass validation;
- trigger undefined behaviour.

Examples include:

- invalid data types;
- missing mandatory fields;
- impossible numerical values;
- oversized payloads.

---

## Potential Impact

- incorrect predictions;
- runtime failures;
- denial of service.

---

## Mitigation

- strict schema validation;
- mandatory field verification;
- range checking;
- type validation;
- early rejection.

---

# Threat 2 — Adversarial Input Manipulation

## Description

Applicants intentionally manipulate input values to maximise approval probability.

Examples:

- income inflation;
- debt concealment;
- strategic feature manipulation.

---

## Potential Impact

- incorrect approvals;
- increased financial risk.

---

## Mitigation

- deterministic compliance rules;
- manual review escalation;
- future integration with external verification services.

---

# Threat 3 — Compliance Bypass

## Description

An attacker attempts to bypass mandatory legal constraints.

Examples:

- disabling rule evaluation;
- modifying thresholds;
- removing veto logic.

---

## Potential Impact

Illegal automated decisions.

---

## Mitigation

- independent Compliance Engine;
- deterministic rule evaluation;
- immutable decision flow;
- automated testing.

The predictive model never has authority to override compliance.

---

# Threat 4 — Prompt Injection

## Description

Future versions integrating LLMs may receive malicious prompts intended to manipulate generated explanations.

---

## Potential Impact

- hallucinated explanations;
- disclosure of internal prompts;
- misleading customer communications.

---

## Mitigation

Current repository:

Not applicable.

Future architecture:

- deterministic templates;
- retrieval isolation;
- post-generation verification;
- fact checking.

---

# Threat 5 — Hallucinated Explanations

## Description

Generated explanations contain information unsupported by the decision.

---

## Potential Impact

- misleading customers;
- regulatory violations;
- legal liability.

---

## Mitigation

- deterministic explanation generation;
- structured reason codes;
- numerical verification;
- automatic rejection of inconsistent explanations.

---

# Threat 6 — Rule Manipulation

## Description

Unauthorized modification of compliance rules.

---

## Potential Impact

Systematic approval of non-compliant applications.

---

## Mitigation

Recommended production controls:

- version-controlled rules;
- change approval workflow;
- role-based permissions;
- audit logging.

---

# Threat 7 — Audit Log Tampering

## Description

Modification or deletion of historical decisions.

---

## Potential Impact

Loss of traceability.

---

## Mitigation

Architectural principle:

Audit records should be immutable.

Production implementations should include:

- append-only storage;
- cryptographic integrity;
- secure backups;
- restricted write permissions.

---

# Threat 8 — Insider Threats

## Description

Authorized personnel intentionally misuse privileged access.

---

## Potential Impact

- rule modification;
- explanation alteration;
- decision manipulation.

---

## Mitigation

Recommended controls:

- least privilege;
- separation of duties;
- administrative logging;
- periodic reviews.

---

# Threat 9 — Model Replacement

## Description

Replacement of the trained model with an unapproved version.

---

## Potential Impact

Unvalidated decisions.

---

## Mitigation

Recommended production controls:

- model versioning;
- digital signatures;
- deployment approval;
- checksum verification.

---

# Threat 10 — Data Poisoning

## Description

Training data intentionally manipulated.

---

## Potential Impact

Biased or degraded predictive behaviour.

---

## Mitigation

- controlled datasets;
- dataset validation;
- reproducible training;
- independent evaluation.

---

# Threat 11 — Privacy Leakage

## Description

Sensitive customer information disclosed through explanations or logs.

---

## Potential Impact

GDPR violations.

---

## Mitigation

- minimum necessary information;
- structured explanations;
- restricted logging;
- future data masking.

---

# Threat 12 — Denial of Service

## Description

Repeated requests intended to exhaust system resources.

---

## Potential Impact

Reduced availability.

---

## Mitigation

Recommended production measures:

- rate limiting;
- request throttling;
- caching;
- autoscaling;
- monitoring.

---

# Threat 13 — Dependency Vulnerabilities

## Description

Third-party libraries contain known vulnerabilities.

---

## Potential Impact

System compromise.

---

## Mitigation

Recommended practices:

- dependency scanning;
- regular updates;
- vulnerability monitoring;
- Software Bill of Materials (SBOM).

---

# Threat 14 — Unauthorized Repository Modification

## Description

Malicious changes introduced into source code.

---

## Potential Impact

Supply chain compromise.

---

## Mitigation

Recommended practices:

- protected branches;
- mandatory code review;
- signed commits;
- CI validation.

---

# Threat 15 — Business Logic Abuse

## Description

Users exploit valid workflows in unintended ways.

---

## Example

Repeatedly submitting modified applications until approval is obtained.

---

## Mitigation

Production recommendations:

- submission history;
- anomaly detection;
- behavioural analytics;
- manual investigation.

---

# Security Controls Summary

| Threat | Mitigation |
|----------|------------|
| Invalid Inputs | Schema Validation |
| Adversarial Inputs | Compliance Rules |
| Compliance Bypass | Deterministic Veto |
| Hallucinations | Fact Checker |
| Rule Tampering | Version Control |
| Audit Manipulation | Immutable Logging |
| Insider Threats | Least Privilege |
| Model Replacement | Model Versioning |
| Data Poisoning | Dataset Validation |
| Privacy Leakage | Data Minimisation |
| DoS | Rate Limiting |
| Dependency Risk | Vulnerability Scanning |

---

# Residual Risks

No software system can eliminate all risk.

Residual risks include:

- novel adversarial techniques;
- undiscovered software vulnerabilities;
- zero-day attacks;
- regulatory changes;
- human operational errors.

These risks require continuous monitoring and periodic reassessment.

---

# Security Assumptions

The current repository assumes:

- trusted execution environment;
- authenticated operators;
- validated deployment pipeline;
- secure operating system;
- protected infrastructure.

These assumptions would need to be explicitly verified in production.

---

# Out of Scope

The following topics are intentionally outside the scope of this repository:

- network security;
- cloud infrastructure;
- identity providers;
- database encryption;
- secrets management;
- incident response;
- disaster recovery.

These concerns belong to deployment architecture rather than the application itself.

---

# Security Principles

Throughout the project, the following principles guided architectural decisions:

- Validate all inputs.
- Never trust user-provided data.
- Separate statistical prediction from regulatory decisions.
- Prefer deterministic behaviour where correctness is critical.
- Preserve complete auditability.
- Fail safely under uncertainty.
- Minimise unnecessary complexity.
- Assume every component may eventually fail.

---

# Conclusion

Security within CREDERE is approached as an architectural property rather than a collection of isolated protections.

By combining deterministic compliance, structured explanations, validation layers, human oversight and complete auditability, the system reduces the likelihood that a single failure compromises the integrity of automated credit decisions.

While no system can guarantee absolute security, CREDERE demonstrates how trustworthy AI systems can be designed to anticipate failures, contain their impact and preserve transparency throughout the decision lifecycle.