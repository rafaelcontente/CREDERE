"""Testes do motor de conformidade do CREDERE."""

from __future__ import annotations

import pytest

from credere.compliance import (
    ComplianceGate,
    RuleEngine,
    Severity,
    VetoAction,
    max_effort_rule,
    no_protected_attributes_rule,
)
from credere.compliance.rules import justification_required_rule, max_pd_rule
from credere.scoring.models import (
    CreditApplication,
    Decision,
    DecisionOutcome,
    ReasonCode,
)


def _decision(outcome: DecisionOutcome, with_reasons: bool = True) -> Decision:
    reasons = (
        [ReasonCode(factor="dsti", points=-10, band_label="x")]
        if with_reasons else []
    )
    return Decision(
        applicant_id="C", score=650, outcome=outcome, reason_codes=reasons
    )


def _app(**attrs) -> CreditApplication:
    return CreditApplication(applicant_id="C", attributes=attrs)


# --------------------------------------------------------------------------- #
# Regra: taxa de esforço máxima
# --------------------------------------------------------------------------- #
def test_dsti_alto_com_aprovacao_e_violacao() -> None:
    rule = max_effort_rule(max_dsti=40)
    v = rule.evaluate(_app(dsti=60), _decision(DecisionOutcome.APPROVED))
    assert v is not None
    assert v.severity is Severity.HARD


def test_dsti_alto_sem_aprovacao_nao_viola() -> None:
    rule = max_effort_rule(max_dsti=40)
    # Se já foi recusado, não há nada a vetar.
    v = rule.evaluate(_app(dsti=60), _decision(DecisionOutcome.DECLINED))
    assert v is None


def test_dsti_dentro_do_limite_nao_viola() -> None:
    rule = max_effort_rule(max_dsti=40)
    v = rule.evaluate(_app(dsti=30), _decision(DecisionOutcome.APPROVED))
    assert v is None


def test_dsti_ausente_nao_viola() -> None:
    rule = max_effort_rule(max_dsti=40)
    v = rule.evaluate(_app(rendimento_mensal=2000),
                      _decision(DecisionOutcome.APPROVED))
    assert v is None


# --------------------------------------------------------------------------- #
# Regra: não-discriminação
# --------------------------------------------------------------------------- #
def test_atributo_protegido_e_violacao() -> None:
    rule = no_protected_attributes_rule()
    v = rule.evaluate(_app(idade=30, dsti=20),
                      _decision(DecisionOutcome.APPROVED))
    assert v is not None
    assert v.veto_action is VetoAction.FORCE_DECLINE


def test_atributos_neutros_nao_violam() -> None:
    rule = no_protected_attributes_rule()
    v = rule.evaluate(_app(rendimento_mensal=2000, dsti=20),
                      _decision(DecisionOutcome.APPROVED))
    assert v is None


# --------------------------------------------------------------------------- #
# Regra: justificação obrigatória
# --------------------------------------------------------------------------- #
def test_recusa_sem_justificacao_viola() -> None:
    rule = justification_required_rule()
    v = rule.evaluate(_app(dsti=20),
                      _decision(DecisionOutcome.DECLINED, with_reasons=False))
    assert v is not None


def test_recusa_com_justificacao_ok() -> None:
    rule = justification_required_rule()
    v = rule.evaluate(_app(dsti=20),
                      _decision(DecisionOutcome.DECLINED, with_reasons=True))
    assert v is None


# --------------------------------------------------------------------------- #
# Regra SOFT: PD prudencial
# --------------------------------------------------------------------------- #
def test_pd_alta_e_violacao_soft() -> None:
    rule = max_pd_rule(max_pd=0.5)
    v = rule.evaluate(_app(pd=0.7), _decision(DecisionOutcome.APPROVED))
    assert v is not None
    assert v.severity is Severity.SOFT


# --------------------------------------------------------------------------- #
# Motor de regras
# --------------------------------------------------------------------------- #
def test_engine_recolhe_multiplas_violacoes() -> None:
    engine = RuleEngine()
    # DSTI alto + fator protegido → duas violações.
    app = _app(dsti=60, idade=30)
    violations = engine.check(app, _decision(DecisionOutcome.APPROVED))
    names = {v.rule_name for v in violations}
    assert "taxa_esforco_maxima" in names
    assert "nao_discriminacao" in names


def test_engine_sem_regras_nao_viola() -> None:
    engine = RuleEngine(rules=[])
    violations = engine.check(_app(dsti=99), _decision(DecisionOutcome.APPROVED))
    assert violations == []


# --------------------------------------------------------------------------- #
# ComplianceGate — o veto neuro-simbólico
# --------------------------------------------------------------------------- #
def test_gate_veta_dsti_alto() -> None:
    gate = ComplianceGate()
    v = gate.evaluate(_app(dsti=60), _decision(DecisionOutcome.APPROVED))
    assert v.vetoed is True
    assert v.final_outcome == "revisao_manual"
    assert v.original_outcome == "aprovado"


def test_gate_veta_e_recusa_por_discriminacao() -> None:
    gate = ComplianceGate()
    v = gate.evaluate(_app(codigo_postal="1200", dsti=20),
                      _decision(DecisionOutcome.APPROVED))
    assert v.vetoed is True
    # Não-discriminação força recusa (ação mais severa).
    assert v.final_outcome == "recusado"


def test_gate_decisao_conforme_passa() -> None:
    gate = ComplianceGate()
    v = gate.evaluate(_app(dsti=25), _decision(DecisionOutcome.APPROVED))
    assert v.vetoed is False
    assert v.final_outcome == "aprovado"
    assert v.is_compliant is True


def test_gate_simbolico_ganha_ao_estatistico() -> None:
    # O cerne: o modelo aprova, a regra dura proíbe → a regra ganha.
    gate = ComplianceGate()
    aprovacao_do_modelo = _decision(DecisionOutcome.APPROVED)
    v = gate.evaluate(_app(dsti=70), aprovacao_do_modelo)
    assert aprovacao_do_modelo.outcome is DecisionOutcome.APPROVED  # intacto
    assert v.final_outcome != "aprovado"  # mas o veredicto veta


def test_gate_gera_alertas() -> None:
    gate = ComplianceGate()
    v = gate.evaluate(_app(dsti=60), _decision(DecisionOutcome.APPROVED))
    assert len(v.alerts) >= 1
    assert any("VETO" in a for a in v.alerts)


def test_gate_violacao_soft_nao_veta() -> None:
    gate = ComplianceGate()
    # PD alta é SOFT: gera aviso mas não veta.
    v = gate.evaluate(_app(pd=0.7, dsti=20), _decision(DecisionOutcome.APPROVED))
    assert v.vetoed is False
    assert v.final_outcome == "aprovado"
    assert any("AVISO" in a for a in v.alerts)


def test_verdict_tem_disclaimer() -> None:
    gate = ComplianceGate()
    v = gate.evaluate(_app(dsti=25), _decision(DecisionOutcome.APPROVED))
    assert "jurídico" in v.disclaimer.lower()
