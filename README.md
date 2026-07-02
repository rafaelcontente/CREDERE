# CREDERE — Neuro-Symbolic Compliance & Hallucination-Free Explanations for Credit Scoring

> Two production-grade modules from the CREDERE credit-scoring system, showcasing
> how to make automated credit decisions **legally defensable** and **explainable
> without hallucination** — the two hardest problems in regulated ML.

![Decision Tree](docs/arvore_decisao.png)

*Full system architecture: a candidate flows through input guardrails, scoring,
compliance (with veto power), output guardrails, human-in-the-loop, and an
immutable audit ledger.*

---

## The Compliance Dilemma

Black-box models — XGBoost, neural networks — optimise for predictive accuracy,
but they **cannot guarantee legal limits**. A model might learn that approving a
loan with a 60% debt-service-to-income ratio maximises short-term profit, even
though the law forbids it. You cannot "train away" a hard legal constraint: a
probability is not a guarantee.

**CREDERE's answer: a neuro-symbolic compliance engine that gives the law veto
power over statistics.**

The statistical model proposes a decision. A deterministic rule engine then
checks it against hard legal and policy rules (debt-service limits, prohibition
of protected attributes, mandatory justification). When the model and a hard rule
conflict, **the rule wins, every time** — the decision is vetoed and forced to
review or refusal, with an alert.

```python
from credere.compliance import ComplianceGate

# The model approved this applicant (score 700) — but DSTI is 60%, over the legal 40% limit
verdict = ComplianceGate().evaluate(application, decision)

print(verdict.original_outcome)   # aprovado  (what the model wanted)
print(verdict.final_outcome)      # revisao_manual  (what the law forces)
print(verdict.vetoed)             # True
```

This is what makes the system defensable under the EU AI Act's high-risk regime:
the deterministic layer is auditable and cannot be overridden by a confident
model. **18 automated tests** cover the veto logic against failure scenarios.

---

## The Explanation Headache

The EU GDPR (Article 22) gives people the right to an explanation of automated
decisions. The tempting solution is to ask an LLM (Llama, GPT) to "explain why
this loan was refused." **This is a legal landmine.**

An LLM can hallucinate — it might write "your debt ratio of 38%" when the real
figure was 42%, or invent a factor that never contributed. In a chatbot, a
hallucination is an annoyance. **In a credit-refusal letter, it is a GDPR
violation and a liability.**

**CREDERE's answer: deterministic templating with fact verification, giving a 0%
hallucination rate on the numbers.**

Every figure in the explanation comes directly from the decision's `reason_codes`
— never generated freely. A fact-checker then compares every number in the text
against the source data and rejects any mismatch.

```python
from credere.explanation import ExplanationGenerator, FactChecker

explanation = ExplanationGenerator().explain_decision(decision)
# "O pedido foi recusado, com um score de 560. Os fatores que mais contribuíram
#  foram: (1) incidentes (com incidentes), contribuição de -100 pontos; ..."

result = FactChecker().check(explanation)
print(result.verified)   # True — every number matches the data
```

An optional LLM refiner can improve fluency, but it may **only rephrase** — every
paraphrase is re-verified against the facts, and any hallucination is rejected in
favour of the deterministic text. **14 automated tests** cover generation and
hallucination detection.

---

## Try it — isolated demo (no full pipeline needed)

The demo uses a static dictionary that simulates the ML layer's output. Edit the
values to see the modules react.

```bash
pip install -e .
python run_demo_isolated.py
```

You'll see the explanation engine produce a Portuguese justification, and the
compliance engine **veto** a decision when a hard rule is broken.

---

## What this is part of

These two modules belong to **CREDERE**, a 16-module credit-scoring system built
with a focus on explainability, fairness, and regulatory compliance. The full
system was trained and validated on real data (Kaggle's Loan Prediction dataset),
with **240 automated tests** and **26 validation batteries** covering security,
privacy, calibration, fairness, drift, and AI Act coverage.

See the accompanying documents:
- **CREDERE_Documento_Sistema.pdf** — decision tree, all tests, AI Act checklist
- **CREDERE_Documentacao_Validacao.pdf** — validation results on real data

---

## Honesty note

The demonstration dataset measures **historical loan approval**, not real default
— so the model replicates a bank's past decisions (bias included), which is
exactly why the fairness and compliance layers matter. Production use would
require retraining on real default data and independent legal validation. This is
stated plainly in the documents, because a system you can trust is one that
declares its limits.
