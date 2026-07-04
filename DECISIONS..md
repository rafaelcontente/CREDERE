# Architectural & Design Decisions

> **Why CREDERE was designed this way.**

This document records the major engineering decisions taken during the design and implementation of the CREDERE prototype.

Rather than presenting only *what* was built, this document explains *why* specific technologies, algorithms and architectural patterns were selected, together with the trade-offs that influenced each decision.

The goal is to preserve architectural reasoning as a permanent project artifact.

---

# Design Philosophy

CREDERE was never intended to be "just another credit-scoring model."

The project was designed around a broader question:

> **How can AI systems make automated financial decisions that remain trustworthy, explainable and legally defensible?**

From the beginning, architectural decisions were evaluated not only by predictive performance but also by:

- Explainability
- Auditability
- Regulatory compliance
- Engineering simplicity
- Reproducibility
- Maintainability

---

# Decision 1 — Separate Prediction from Decision-Making

## Decision

The predictive model is **not responsible** for the final customer decision.

Instead, it produces:

- score
- probability
- structured reason codes

The final decision is produced by deterministic post-processing layers.

---

## Why

A statistical model optimises prediction.

A bank must optimise legal compliance.

Those objectives are different.

Allowing the model to directly approve or reject applications would couple statistical inference with legal responsibility.

Separating both concerns produces:

- better auditability
- deterministic behaviour
- regulatory transparency
- simpler validation

---

## Alternatives Considered

### End-to-end ML

Rejected.

Although simpler, it cannot guarantee compliance with mandatory legal constraints.

---

### Pure Rule-Based Decision System

Rejected.

Deterministic systems alone cannot model complex credit risk accurately.

---

## Final Choice

Hybrid Neuro-Symbolic Architecture.

Machine learning predicts.

Deterministic logic decides.

---

# Decision 2 — Compliance Engine Uses Deterministic Rules

## Decision

Legal constraints are implemented as deterministic rules.

---

## Why

Financial regulation contains hard constraints rather than probabilities.

Examples include:

- maximum debt-service ratio
- prohibited protected attributes
- mandatory documentation
- internal banking policies

These constraints must never be violated regardless of model confidence.

---

## Alternatives Considered

### LLM-based legal reasoning

Rejected.

LLMs cannot guarantee deterministic outputs.

---

### Learned compliance classifier

Rejected.

A statistical model cannot guarantee perfect enforcement of legal rules.

---

## Final Choice

Explicit rule engine with veto authority.

---

# Decision 3 — Compliance Has Veto Power

## Decision

Compliance can override any statistical prediction.

---

## Why

Legal obligations always have higher priority than predictive optimisation.

If a conflict exists:

Law wins.

Always.

---

## Benefits

- deterministic behaviour
- predictable validation
- legal defensibility
- simpler audits

---

# Decision 4 — Deterministic Explanation Generation

## Decision

Customer explanations are generated using templates and structured data.

---

## Why

Financial explanations must be factually correct.

Natural language generation alone cannot guarantee numerical accuracy.

Every value presented to customers must originate directly from the decision object.

---

## Alternatives Considered

### GPT / Llama explanation

Rejected for primary generation.

Although fluent, hallucinations remain possible.

---

### SHAP visualisations only

Rejected.

Useful for engineers.

Poor customer communication.

---

## Final Choice

Template-driven explanations.

---

# Decision 5 — Fact Verification

## Decision

Every explanation is verified before publication.

---

## Why

Even deterministic systems deserve validation.

Verification provides an additional safety layer.

Every number appearing in the explanation must match the original decision.

---

## Benefits

- zero numerical hallucinations
- higher trust
- reproducible outputs

---

# Decision 6 — Human-in-the-Loop

## Decision

Borderline and exceptional cases require human review.

---

## Why

Responsible AI does not eliminate expert judgement.

Human supervision remains essential whenever:

- confidence is low
- regulation requires oversight
- conflicting evidence exists

---

## Alternatives Considered

### Fully autonomous approval

Rejected.

Too risky for regulated environments.

---

# Decision 7 — Modular Architecture

## Decision

Compliance, explanation, validation and auditing are independent modules.

---

## Why

Small, specialised components are easier to:

- understand
- test
- replace
- validate

This also reduces coupling between business logic and machine learning.

---

# Decision 8 — Logistic Regression as Baseline

## Decision

Logistic Regression was selected as the baseline predictive model.

---

## Why

Credit scoring has historically relied on logistic regression because it offers:

- interpretability
- stability
- calibration
- regulatory acceptance

It provides an excellent benchmark against more complex models.

---

## Alternatives Considered

### Random Forest

Higher complexity.

Lower interpretability.

---

### Neural Networks

Excellent predictive power.

Poor explainability.

---

### XGBoost / LightGBM

Very competitive.

Higher complexity.

Less transparent.

---

## Final Choice

Logistic Regression as baseline.

Gradient boosting considered as future extension.

---

# Decision 9 — Public Dataset

## Decision

The prototype uses the Kaggle Loan Prediction dataset.

---

## Why

A public dataset allows:

- reproducibility
- transparency
- independent verification

Readers can reproduce every experiment.

---

## Known Limitation

The dataset predicts historical approval decisions rather than actual default events.

This limitation is explicitly documented throughout the project.

---

# Decision 10 — Repository Focus

## Decision

Only two modules are published.

---

## Why

The objective of this repository is to demonstrate architectural patterns rather than expose the entire research platform.

Publishing only the Compliance and Explanation engines keeps the repository:

- concise
- understandable
- technically focused

---

# Decision 11 — Extensive Automated Testing

## Decision

Every critical component is validated through automated tests.

---

## Why

Trustworthy AI requires evidence.

Tests demonstrate that behaviour remains stable under:

- normal conditions
- edge cases
- failure scenarios

---

## Benefits

- regression protection
- documentation
- reproducibility
- confidence

---

# Decision 12 — Documentation as an Engineering Artifact

## Decision

Architecture, validation and design decisions are documented alongside the source code.

---

## Why

Documentation is part of the software.

Future contributors should understand not only how the system works, but also why architectural choices were made.

---

# Decision 13 — Simplicity Before Complexity

## Decision

Whenever two approaches achieve similar outcomes, the simpler solution is preferred.

---

## Why

Simple systems are easier to:

- validate
- audit
- maintain
- explain

Complexity should only be introduced when it provides measurable value.

---

# Decision 14 — AI as Decision Support, Not Decision Replacement

## Decision

The system augments human decision-making rather than replacing it.

---

## Why

Financial decisions often involve ethical, legal and contextual considerations beyond statistical prediction.

Human expertise remains essential for exceptional cases.

---

# Lessons Learned

Several lessons emerged during the development of CREDERE.

- High predictive performance does not guarantee trustworthy AI.
- Explainability must be engineered rather than added afterwards.
- Compliance should be treated as a first-class architectural component.
- Simplicity often improves robustness.
- Deterministic safeguards complement statistical intelligence.
- Documentation is as important as implementation.

---

# Future Decisions

The broader CREDERE roadmap includes future architectural decisions around:

- Knowledge Graph integration
- Retrieval-Augmented Generation
- Long-term memory
- Mixture of Experts
- World Models
- Continuous monitoring
- Drift detection
- Multi-agent orchestration

These capabilities will be evaluated using the same design philosophy documented here.

---

# Closing Statement

Every architectural decision in CREDERE reflects a single engineering principle:

> **AI systems deployed in regulated environments should optimise not only for predictive performance, but also for transparency, reproducibility, accountability and human trust.**

This document records the reasoning behind those choices so that future contributors can understand not only *how* the system works, but *why* it was built this way.