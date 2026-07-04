
# Validation Strategy

> **Trustworthy AI requires evidence, not claims.**

This document summarises the validation strategy adopted for the CREDERE prototype, the tests performed, the results obtained, known limitations, and the distinction between demonstrated capabilities and future research objectives.

Unlike many AI projects that report only predictive performance, CREDERE validates the entire decision pipeline, including compliance, explainability, fairness, robustness, security, and regulatory readiness.

---

# Validation Philosophy

CREDERE follows a simple principle:

> **Every architectural claim should be supported by objective evidence whenever possible.**

Validation therefore extends beyond machine learning metrics to include:

- Predictive performance
- Compliance correctness
- Explainability
- Fairness
- Robustness
- Security
- Human oversight
- Regulatory readiness

---

# Validation Scope

Validation was performed at multiple levels.

| Level | Purpose |
|---------|----------|
| Unit Tests | Validate individual modules |
| Integration Tests | Validate interaction between modules |
| System Tests | Validate the complete decision pipeline |
| Adversarial Tests | Evaluate robustness against abnormal inputs |
| Regulatory Validation | Assess alignment with the EU AI Act |
| Documentation Validation | Verify transparency and reproducibility |

---

# Validation Categories

The complete prototype was evaluated through multiple validation batteries covering the most relevant dimensions of trustworthy AI.

These include:

- Predictive performance
- Explainability
- Compliance
- Fairness
- Robustness
- Security
- Human oversight
- Transparency
- AI Act readiness
- System integrity

Together, these provide evidence that the system behaves consistently under both normal and adverse conditions.

---

# Predictive Performance

The predictive model was evaluated using standard binary classification metrics.

Reported results include:

| Metric | Result |
|---------|---------:|
| ROC-AUC | **0.805** |
| Accuracy | **82%** |

These values indicate good discrimination between approved and rejected applications while remaining interpretable and suitable for regulated environments. :contentReference[oaicite:0]{index=0}

---

# Explainability Validation

The explanation subsystem was validated independently from the predictive model.

Validation objectives included:

- Correct explanation generation
- Numerical consistency
- Template integrity
- Fact verification
- Hallucination detection

The public repository includes automated tests covering deterministic explanation generation and fact verification.

Expected behaviour:

- Every explanation originates from structured decision data.
- Every numerical value is verified against the original decision object.
- Any mismatch causes the explanation to be rejected.

---

# Compliance Validation

The Compliance Engine was validated using deterministic rule evaluation.

Typical scenarios include:

- Excessive Debt-Service-to-Income ratio
- Mandatory rule violations
- Protected attribute exclusion
- Manual review escalation

Validation confirms that deterministic rules always override statistical predictions whenever a conflict exists.

This behaviour is fundamental to the neuro-symbolic architecture.

---

# Fairness Validation

Fairness validation focused on detecting potential discriminatory behaviour.

The validation process included:

- exclusion of protected attributes from training,
- detection of proxy variables,
- disparate impact analysis,
- subgroup comparison,
- intersectional analysis.

Residual bias inherited from the historical dataset is explicitly documented rather than hidden. :contentReference[oaicite:1]{index=1}

---

# Robustness Validation

Robustness tests evaluated how the system behaves under abnormal or unexpected conditions.

Scenarios included:

- invalid values,
- malformed requests,
- missing fields,
- extreme combinations of inputs,
- boundary conditions.

Expected behaviour:

- reject invalid inputs,
- fail safely,
- preserve deterministic behaviour.

---

# Security Validation

Security validation focused on protecting the integrity of the decision process.

Representative scenarios included:

- adversarial inputs,
- decision manipulation attempts,
- model gaming,
- immutable audit verification,
- log tampering detection.

The objective is not only to prevent attacks, but also to guarantee traceability after an incident. :contentReference[oaicite:2]{index=2}

---

# Human Oversight Validation

The prototype validates that uncertain decisions are escalated instead of being automatically finalised.

Applications with prediction confidence close to the decision boundary are correctly identified and forwarded for manual review together with a structured summary for the analyst. This demonstrates effective human oversight aligned with the expectations for high-risk AI systems. :contentReference[oaicite:3]{index=3}

---

# AI Act Readiness

The system documentation was assessed against the principal technical expectations of the European AI Act for high-risk AI systems.

The prototype demonstrates coverage for:

- Risk management
- Data governance
- Technical documentation
- Logging
- Transparency
- Human oversight
- Accuracy
- Robustness
- Cybersecurity
- Fairness

Overall, **8 of the 10** evaluated technical requirements are covered within the prototype. The remaining items—formal conformity assessment and independent legal validation—necessarily require external organisations and therefore remain outside the scope of this repository. :contentReference[oaicite:4]{index=4}

---

# Transparency Validation

Transparency was evaluated by checking whether all information required to understand system behaviour is available.

The documentation includes:

- system description,
- dataset description,
- performance metrics,
- subgroup analysis,
- limitations,
- human oversight,
- bias mitigation.

The internal checklist achieved full coverage for the evaluated transparency requirements. :contentReference[oaicite:5]{index=5}

---

# Temporal Robustness

A preliminary sensitivity analysis compared model performance under random data partitioning and sequential file ordering.

Results showed a reduction in ROC-AUC from **0.805** to **0.729**.

However, the dataset does **not** contain genuine timestamps. Consequently, the sequential ordering serves only as a methodological placeholder and should **not** be interpreted as evidence of temporal drift or seasonality. Future production deployments should repeat this analysis using real chronological data. :contentReference[oaicite:6]{index=6}

---

# Test Coverage

Validation includes three complementary levels.

## Unit Tests

Validate isolated components.

Examples:

- Compliance rules
- Explanation generation
- Fact verification
- Utility functions

---

## Integration Tests

Validate interaction between modules.

Examples:

- Prediction → Compliance
- Compliance → Explanation
- Explanation → Fact Checker
- Human Review workflow

---

## End-to-End Tests

Validate the complete pipeline.

```
Application

↓

Validation

↓

Prediction

↓

Compliance

↓

Explanation

↓

Verification

↓

Audit

↓

Decision
```

These tests confirm that all modules operate together as expected.

---

# Failure Scenarios

Validation deliberately includes failure conditions.

Examples include:

| Scenario | Expected Behaviour |
|-----------|-------------------|
| Missing input | Reject request |
| Invalid data type | Reject request |
| Compliance violation | Veto prediction |
| Missing documentation | Manual review |
| Explanation mismatch | Reject explanation |
| Internal inconsistency | Fail closed |

The system is intentionally designed to fail safely rather than produce uncertain outputs.

---

# Known Limitations

The current prototype intentionally documents its limitations.

## Dataset

The demonstration dataset reflects historical loan approval decisions rather than actual default outcomes.

Consequently, the predictive model reproduces historical institutional behaviour rather than true credit risk.

---

## Legal Validation

This repository does not constitute legal advice.

Independent legal review remains necessary before production deployment.

---

## Regulatory Certification

Formal conformity assessment under the EU AI Act is outside the scope of this technical prototype.

Certification requires external notified bodies and regulatory procedures. :contentReference[oaicite:7]{index=7}

---

## Production Validation

The public repository demonstrates architectural patterns.

Deployment in production would require:

- institution-specific data,
- production monitoring,
- continuous calibration,
- operational governance,
- independent compliance assessment.

---

# Evidence Matrix

The table below distinguishes validated capabilities from future work.

| Capability | Status |
|------------|--------|
| Credit prediction | ✅ Demonstrated |
| Deterministic compliance | ✅ Demonstrated |
| Compliance veto | ✅ Demonstrated |
| Deterministic explanations | ✅ Demonstrated |
| Fact verification | ✅ Demonstrated |
| Human review workflow | ✅ Demonstrated |
| Auditability | ✅ Demonstrated |
| AI Act documentation mapping | ✅ Demonstrated |
| Public reproducibility | ✅ Demonstrated |
| Production deployment | ⚠ Not demonstrated |
| Continuous monitoring | ⚠ Future work |
| Drift monitoring with real temporal data | ⚠ Future work |
| Formal AI Act conformity assessment | ⚠ External process |
| Independent legal validation | ⚠ External process |

---

# What Has Been Demonstrated

The current repository provides objective evidence that:

- deterministic compliance can override statistical predictions;
- customer explanations can be generated without factual hallucinations;
- numerical consistency can be automatically verified;
- human oversight can be integrated into the decision process;
- regulatory documentation can be systematically produced;
- trustworthy AI principles can be implemented through software architecture.

---

# What Has Not Been Demonstrated

The following claims are intentionally **not** made by this project:

- that the predictive model is production-ready;
- that the system has undergone formal regulatory certification;
- that legal compliance has been independently verified;
- that performance generalises to all financial institutions;
- that temporal robustness has been validated on real chronological datasets.

These items remain outside the scope of the current prototype and are explicitly acknowledged to preserve transparency.

---

# Conclusion

Validation in CREDERE extends far beyond measuring predictive accuracy.

The project evaluates not only whether the model predicts correctly, but also whether the surrounding decision system behaves responsibly, transparently and consistently under regulatory expectations.

This distinction reflects the central philosophy of the project:

> **A trustworthy AI system is validated not only by how accurately it predicts, but also by how reliably it explains, complies, records and escalates its decisions.**