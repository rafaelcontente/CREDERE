
# CREDERE Case Study

**Designing Trustworthy AI for Credit Scoring through Neuro-Symbolic Compliance and Hallucination-Free Explanations**

---

> *Artificial Intelligence can predict.
>
> But can it justify?
>
> Can it comply with the law?
>
> Can it be trusted?*

These questions motivated the creation of **CREDERE**, a research and software engineering project exploring how trustworthy AI systems can be designed for regulated financial decision-making.

Rather than focusing solely on predictive performance, CREDERE investigates a broader engineering challenge:

> **How do we build AI systems whose decisions can be understood, verified, audited and defended?**

---

# Executive Summary

Credit scoring has become one of the most common applications of Machine Learning.

Modern statistical models are capable of predicting loan approval outcomes with impressive accuracy. However, accuracy alone is insufficient in regulated domains.

Financial institutions operate under strict legal requirements. Customers affected by automated decisions increasingly expect meaningful explanations. Regulators demand transparency, accountability and human oversight.

Traditional black-box machine learning models address none of these concerns directly.

CREDERE was created to explore an alternative.

Instead of relying exclusively on statistical prediction, the project combines Machine Learning with deterministic symbolic reasoning, producing a **neuro-symbolic architecture** where legal constraints always take precedence over model predictions and customer explanations are generated without factual hallucinations.

The public repository demonstrates two production-oriented components extracted from the broader CREDERE platform:

- Compliance Engine
- Hallucination-Free Explanation Engine

Together, they illustrate how trustworthy AI can be engineered through software architecture rather than predictive models alone.

---

# Background

Artificial Intelligence has transformed decision support across finance, healthcare and public administration.

Yet regulated sectors face a persistent dilemma.

The most accurate predictive models are often the least interpretable.

Gradient Boosting, Random Forests and Deep Neural Networks optimise prediction accuracy but cannot guarantee compliance with external legal requirements.

Likewise, Large Language Models generate remarkably fluent explanations but cannot guarantee factual correctness.

For entertainment software this may be acceptable.

For automated credit decisions it is not.

An incorrect explanation or an illegal approval may have significant legal and financial consequences.

CREDERE emerged from the observation that these two problems are fundamentally architectural rather than statistical.

---

# The Engineering Challenge

The project focused on two independent—but closely related—problems.

## Challenge 1

### Statistical models cannot enforce legal constraints.

A predictive model may recommend approving a customer whose debt ratio exceeds a legally accepted threshold.

From the model's perspective this prediction maximises statistical performance.

From a regulatory perspective it is unacceptable.

The challenge therefore becomes:

> **How can deterministic legal requirements override probabilistic predictions?**

---

## Challenge 2

### Language models hallucinate.

Modern LLMs generate convincing natural language.

Unfortunately they also generate convincing mistakes.

For customer explanations this creates unacceptable risks.

An explanation may contain:

- incorrect numbers
- invented reasons
- unsupported statements

Such behaviour directly conflicts with transparency requirements established by regulations such as GDPR.

The challenge therefore becomes:

> **How can explanations remain both understandable and factually perfect?**

---

# Project Objectives

Before implementation began, the project established several engineering principles.

The system should:

- remain modular;
- remain auditable;
- preserve human oversight;
- produce deterministic legal compliance;
- generate reproducible explanations;
- separate prediction from regulation;
- fail safely under uncertainty.

Importantly, predictive accuracy was **never** considered the sole optimisation target.

---

# Why a Neuro-Symbolic Architecture?

Many AI systems treat regulation as another prediction problem.

CREDERE deliberately does not.

Instead, statistical learning answers one question:

> *What is the most likely decision?*

Symbolic reasoning answers another:

> *Is this decision legally acceptable?*

The final outcome emerges only after both layers agree.

This separation dramatically simplifies auditing while preventing statistical optimisation from violating deterministic rules.

---

# Architecture Overview

The complete decision pipeline follows a layered architecture.

```
Application

↓

Input Validation

↓

Machine Learning Prediction

↓

Compliance Engine

↓

Explanation Engine

↓

Fact Checker

↓

Human Review (when required)

↓

Audit Log

↓

Final Decision
```

Each layer has a clearly defined responsibility.

No component attempts to solve every problem.

This separation of concerns became one of the project's defining characteristics.

---

# Why Not Use an LLM?

One obvious question emerged during development:

> Why not simply ask GPT or another LLM to explain every decision?

Because fluency is not correctness.

Even rare factual hallucinations become unacceptable when explanations form part of legally significant customer communications.

CREDERE therefore adopts deterministic templates whose numerical values originate directly from structured decision objects.

An optional language model may improve wording in future versions, but every generated sentence would still require deterministic fact verification before being accepted.

The architecture deliberately prioritises correctness over linguistic elegance.

---

# Key Engineering Decisions

Several design decisions shaped the final architecture.

## Compliance before Explanation

Customers should never receive explanations for decisions that violate regulatory constraints.

Compliance therefore precedes explanation generation.

---

## Rules Override Statistics

Legal constraints always have veto power.

This prevents highly confident—but legally invalid—predictions from becoming final decisions.

---

## Templates before Generation

Natural language generation is restricted to deterministic templates.

Every number originates from structured decision data.

---

## Verification before Publication

Every generated explanation undergoes numerical verification before it becomes visible.

Incorrect explanations are rejected rather than corrected heuristically.

---

## Human Oversight

Uncertain decisions are escalated rather than automatically finalised.

The system supports humans.

It does not replace them.

---

# Development Journey

The project evolved through several distinct phases.

## Phase 1

Problem definition.

Understanding regulatory requirements.

---

## Phase 2

Dataset exploration.

Feature engineering.

Predictive modelling.

---

## Phase 3

System architecture.

Definition of modular responsibilities.

---

## Phase 4

Compliance Engine implementation.

---

## Phase 5

Explanation Engine implementation.

---

## Phase 6

Fact Checker development.

---

## Phase 7

Validation and testing.

---

## Phase 8

Documentation and publication.

---

# Validation Results

Evaluation focused on architectural behaviour rather than prediction alone.

Key observations included:

- deterministic compliance consistently overrides conflicting predictions;
- explanations remain numerically consistent;
- factual hallucinations are eliminated through verification;
- automated tests reproduce expected behaviour across representative scenarios.

The public benchmark demonstrates the feasibility of combining statistical prediction with deterministic governance.

---

# Lessons Learned

Several important lessons emerged during development.

## Accuracy is only one metric.

High predictive performance does not guarantee trustworthy behaviour.

---

## Compliance cannot be learned probabilistically.

Legal requirements require deterministic enforcement.

---

## Explainability requires engineering.

Producing reliable explanations proved significantly harder than generating predictions.

---

## Verification matters more than generation.

Generating explanations is relatively easy.

Verifying them is considerably more important.

---

## Simplicity improves trust.

Many complex architectural alternatives were discarded in favour of simpler deterministic solutions.

---

# Trade-Offs

Every engineering decision introduced trade-offs.

| Decision | Benefit | Cost |
|----------|----------|------|
| Deterministic Compliance | Legal certainty | Reduced flexibility |
| Template Explanations | Zero hallucinations | Less expressive language |
| Human Review | Improved safety | Additional operational cost |
| Independent Fact Checker | High reliability | Additional processing |

These compromises were accepted intentionally.

---

# What Worked Better Than Expected

Several components exceeded initial expectations.

- Compliance Engine simplicity
- Modular architecture
- Fact verification reliability
- Documentation structure
- Automated validation pipeline

---

# What Was More Difficult

Some challenges proved substantially harder than anticipated.

- Designing meaningful customer explanations
- Balancing simplicity with flexibility
- Mapping regulatory principles into software
- Documenting engineering decisions comprehensively

---

# Current Limitations

The repository intentionally documents its limitations.

The demonstration:

- is not a production banking platform;
- uses historical approval data rather than default outcomes;
- has not undergone formal regulatory certification;
- requires institution-specific validation before deployment.

These limitations are explicitly acknowledged to preserve transparency.

---

# Broader Impact

Although developed for credit scoring, the architectural concepts generalise well to other regulated domains.

Potential applications include:

- Banking
- Insurance
- Healthcare
- Government Services
- Public Administration
- Recruitment
- Risk Assessment
- Regulatory Technology (RegTech)

Any domain combining statistical prediction with legal constraints may benefit from similar architectural principles.

---

# Future Directions

Several extensions remain under consideration.

These include:

- Knowledge Graph integration
- Retrieval-Augmented Generation
- Interactive explanation dashboards
- Continuous monitoring
- Drift detection
- REST APIs
- Policy management interfaces
- Enterprise deployment

Each future component will preserve the project's core philosophy of deterministic trustworthiness.

---

# What This Project Demonstrates

CREDERE does not claim to solve every challenge associated with trustworthy AI.

Instead, it demonstrates that several longstanding problems can be substantially reduced through careful software engineering.

Rather than replacing machine learning, deterministic reasoning complements it.

Rather than replacing human judgement, automation supports it.

Rather than generating persuasive explanations, the system produces verifiable ones.

These principles define the project's contribution.

---

# Final Reflections

Modern Artificial Intelligence increasingly excels at making predictions.

Yet societies rarely judge decision systems solely by their accuracy.

They also ask:

- Was the decision legal?
- Can it be explained?
- Can it be verified?
- Who is accountable?
- Can a human intervene?

These questions lie beyond traditional machine learning.

They belong to software architecture.

CREDERE was created to explore precisely this intersection between Artificial Intelligence, software engineering and trustworthy decision-making.

Its central premise is simple:

> **An AI system should not only predict correctly—it should also justify, verify and defend every decision it makes.**

That principle guided every architectural decision throughout the project and continues to define its future evolution.

---

**Created, Architected and Engineered by Rafael Paredes**