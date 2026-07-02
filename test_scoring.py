"""Testes do motor de scoring do CREDERE."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from credere.scoring import (
    CreditApplication,
    DecisionOutcome,
    FactorType,
    ScoreBand,
    ScoreCard,
    ScoreFactor,
    ScoringEngine,
    build_example_scorecard,
    check_factor_name,
    generate_synthetic_application,
)
from credere.scoring.exceptions import ScoreCardError


# --------------------------------------------------------------------------- #
# Escalões (ScoreBand / ScoreFactor)
# --------------------------------------------------------------------------- #
def test_band_numerico_match() -> None:
    band = ScoreBand(min_value=800, max_value=1500, points=40)
    assert band.matches_numeric(1000) is True
    assert band.matches_numeric(1500) is False  # max é exclusive
    assert band.matches_numeric(700) is False


def test_factor_pontua_valor() -> None:
    factor = ScoreFactor(
        name="rendimento", factor_type=FactorType.NUMERIC,
        bands=[
            ScoreBand(max_value=1000, points=-50, label="baixo"),
            ScoreBand(min_value=1000, points=50, label="alto"),
        ],
    )
    points, label = factor.score(1500)
    assert points == 50
    assert label == "alto"


def test_factor_valor_em_falta_usa_default() -> None:
    factor = ScoreFactor(
        name="x", factor_type=FactorType.NUMERIC, default_points=-10,
        bands=[ScoreBand(min_value=0, points=20)],
    )
    points, label = factor.score(None)
    assert points == -10
    assert label == "valor em falta"


def test_factor_categorico() -> None:
    factor = ScoreFactor(
        name="contrato", factor_type=FactorType.CATEGORICAL,
        bands=[
            ScoreBand(categories=["efetivo"], points=40, label="efetivo"),
            ScoreBand(categories=["recibos", "temporario"], points=-20,
                      label="precário"),
        ],
    )
    assert factor.score("efetivo")[0] == 40
    assert factor.score("temporario")[0] == -20


def test_factor_peso_multiplica() -> None:
    factor = ScoreFactor(
        name="x", factor_type=FactorType.NUMERIC, weight=2.0,
        bands=[ScoreBand(min_value=0, points=30)],
    )
    points, _ = factor.score(5)
    assert points == 60  # 30 * 2.0


# --------------------------------------------------------------------------- #
# ScoreCard — validação
# --------------------------------------------------------------------------- #
def test_scorecard_sem_fatores_rejeitado() -> None:
    with pytest.raises(ValidationError):
        ScoreCard(factors=[])


def test_scorecard_thresholds_incoerentes_rejeitado() -> None:
    factor = ScoreFactor(
        name="x", factor_type=FactorType.NUMERIC,
        bands=[ScoreBand(min_value=0, points=10)],
    )
    with pytest.raises(ValidationError):
        ScoreCard(factors=[factor], approve_threshold=500,
                  review_threshold=600)  # approve < review


# --------------------------------------------------------------------------- #
# Motor — decisão e explicabilidade
# --------------------------------------------------------------------------- #
def test_engine_aprova_bom_perfil() -> None:
    engine = ScoringEngine(build_example_scorecard())
    app = CreditApplication(
        applicant_id="bom",
        attributes={"rendimento_mensal": 4000, "dsti": 15,
                    "meses_historico": 90, "incidentes": 0},
    )
    decision = engine.score(app)
    # 500 base +80 +60 +50 +50 = 740 → aprovado.
    assert decision.outcome is DecisionOutcome.APPROVED
    assert decision.score == 740


def test_engine_recusa_mau_perfil() -> None:
    engine = ScoringEngine(build_example_scorecard())
    app = CreditApplication(
        applicant_id="mau",
        attributes={"rendimento_mensal": 650, "dsti": 55,
                    "meses_historico": 6, "incidentes": 4},
    )
    decision = engine.score(app)
    # 500 -60 -80 -20 -120 = 220 → recusado.
    assert decision.outcome is DecisionOutcome.DECLINED


def test_engine_revisao_manual() -> None:
    engine = ScoringEngine(build_example_scorecard())
    app = CreditApplication(
        applicant_id="medio",
        attributes={"rendimento_mensal": 1200, "dsti": 28,
                    "meses_historico": 24, "incidentes": 0},
    )
    decision = engine.score(app)
    # 500 +0 +20 +20 +50 = 590 → entre 580 e 660 → revisão manual.
    assert decision.outcome is DecisionOutcome.MANUAL_REVIEW


def test_decisao_tem_sempre_razoes() -> None:
    engine = ScoringEngine(build_example_scorecard())
    decision = engine.score(generate_synthetic_application("x", seed=1))
    # Uma reason code por fator — a justificação é sempre construída.
    assert len(decision.reason_codes) == 4


def test_top_negative_factors_ordenado() -> None:
    engine = ScoringEngine(build_example_scorecard())
    app = CreditApplication(
        applicant_id="mau",
        attributes={"rendimento_mensal": 650, "dsti": 55,
                    "meses_historico": 6, "incidentes": 4},
    )
    decision = engine.score(app)
    negs = decision.top_negative_factors
    # O pior fator (incidentes, -120) vem primeiro.
    assert negs[0].factor == "incidentes"
    assert negs[0].points == -120


def test_engine_sem_fatores_erro() -> None:
    # Constrói um scorecard válido e depois esvazia (contorna validação).
    card = build_example_scorecard()
    card.factors = []
    with pytest.raises(ScoreCardError):
        ScoringEngine(card)


# --------------------------------------------------------------------------- #
# Fairness guard
# --------------------------------------------------------------------------- #
def test_fairness_deteta_idade() -> None:
    assert check_factor_name("idade") is not None
    assert check_factor_name("age_years") is not None


def test_fairness_deteta_codigo_postal_proxy() -> None:
    assert check_factor_name("codigo_postal") is not None
    assert check_factor_name("zip_code") is not None


def test_fairness_aceita_fator_neutro() -> None:
    assert check_factor_name("rendimento_mensal") is None
    assert check_factor_name("dsti") is None


def test_engine_avisa_fator_protegido() -> None:
    factor_protegido = ScoreFactor(
        name="idade", factor_type=FactorType.NUMERIC,
        bands=[ScoreBand(min_value=18, points=10)],
    )
    factor_ok = ScoreFactor(
        name="rendimento", factor_type=FactorType.NUMERIC,
        bands=[ScoreBand(min_value=0, points=10)],
    )
    engine = ScoringEngine(ScoreCard(factors=[factor_protegido, factor_ok]))
    # O motor assinala o fator 'idade'.
    assert any("idade" in w for w in engine.factor_warnings)
    decision = engine.score(
        CreditApplication(applicant_id="x", attributes={"idade": 30,
                                                         "rendimento": 1000})
    )
    assert len(decision.warnings) >= 1
