"""Testes dos contrafactuais do CREDERE."""

from __future__ import annotations

from credere.scoring import (
    CounterfactualExplainer,
    CreditApplication,
    DecisionOutcome,
    ScoringEngine,
    build_example_scorecard,
)


def _explainer() -> CounterfactualExplainer:
    return CounterfactualExplainer(ScoringEngine(build_example_scorecard()))


def test_contrafactual_perfil_recusado_tem_sugestoes() -> None:
    app = CreditApplication(
        applicant_id="mau",
        attributes={"rendimento_mensal": 650, "dsti": 55,
                    "meses_historico": 6, "incidentes": 2},
    )
    result = _explainer().explain(app)
    assert result.current_outcome is DecisionOutcome.DECLINED
    assert result.points_needed > 0
    assert len(result.suggestions) > 0


def test_sugestoes_ordenadas_por_ganho() -> None:
    app = CreditApplication(
        applicant_id="x",
        attributes={"rendimento_mensal": 650, "dsti": 55,
                    "meses_historico": 6, "incidentes": 2},
    )
    result = _explainer().explain(app)
    gains = [s.points_gain for s in result.suggestions]
    assert gains == sorted(gains, reverse=True)


def test_sugestoes_tem_ganho_positivo() -> None:
    app = CreditApplication(
        applicant_id="x",
        attributes={"rendimento_mensal": 650, "dsti": 55,
                    "meses_historico": 6, "incidentes": 2},
    )
    result = _explainer().explain(app)
    assert all(s.points_gain > 0 for s in result.suggestions)


def test_perfil_otimo_sem_sugestoes() -> None:
    # Perfil já no melhor escalão de tudo → nada a melhorar.
    app = CreditApplication(
        applicant_id="otimo",
        attributes={"rendimento_mensal": 5000, "dsti": 10,
                    "meses_historico": 120, "incidentes": 0},
    )
    result = _explainer().explain(app)
    assert result.current_outcome is DecisionOutcome.APPROVED
    assert result.points_needed == 0
    assert len(result.suggestions) == 0


def test_achievable_quando_ganhos_chegam() -> None:
    app = CreditApplication(
        applicant_id="medio",
        attributes={"rendimento_mensal": 1200, "dsti": 40,
                    "meses_historico": 24, "incidentes": 1},
    )
    result = _explainer().explain(app)
    # Há margem grande de melhoria → atingível.
    assert result.achievable is True


def test_suggestion_tem_texto_legivel() -> None:
    app = CreditApplication(
        applicant_id="x",
        attributes={"rendimento_mensal": 650, "dsti": 55,
                    "meses_historico": 6, "incidentes": 2},
    )
    result = _explainer().explain(app)
    for s in result.suggestions:
        assert s.factor in s.suggestion
        assert "pontos" in s.suggestion
