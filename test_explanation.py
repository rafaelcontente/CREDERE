"""Testes do módulo de explicação do CREDERE."""

from __future__ import annotations

from credere.explanation import (
    ExplanationGenerator,
    FactChecker,
    NaturalExplanation,
    NoOpRefiner,
    SupportingFact,
)
from credere.explanation.refiner import LLMRefiner
from credere.scoring.models import (
    CreditApplication,
    Decision,
    DecisionOutcome,
    ReasonCode,
)


def _decision(outcome=DecisionOutcome.DECLINED):
    return Decision(
        applicant_id="C-1", score=560, outcome=outcome,
        reason_codes=[
            ReasonCode(factor="rendimento_mensal", points=70, band_label="alto"),
            ReasonCode(factor="incidentes", points=60, band_label="sem incidentes"),
            ReasonCode(factor="dsti", points=-30, band_label="elevado"),
            ReasonCode(factor="nulo", points=0, band_label="neutro"),
        ],
    )


# --------------------------------------------------------------------------- #
# Gerador
# --------------------------------------------------------------------------- #
def test_gera_texto_com_score() -> None:
    expl = ExplanationGenerator().explain_decision(_decision())
    assert "560" in expl.text
    assert "recusado" in expl.text


def test_menciona_fatores_por_impacto() -> None:
    expl = ExplanationGenerator().explain_decision(_decision())
    # O fator de maior impacto absoluto (rendimento, 70) vem primeiro.
    assert expl.text.index("rendimento_mensal") < expl.text.index("dsti")


def test_omite_contribuicao_nula() -> None:
    expl = ExplanationGenerator().explain_decision(_decision())
    # O fator com 0 pontos não é mencionado.
    assert "nulo" not in expl.text


def test_respeita_top_n() -> None:
    expl = ExplanationGenerator().explain_decision(_decision(), top_n=2)
    assert len(expl.supporting_facts) == 2


def test_supporting_facts_correspondem() -> None:
    expl = ExplanationGenerator().explain_decision(_decision())
    factores = {f.factor for f in expl.supporting_facts}
    assert "rendimento_mensal" in factores
    assert "nulo" not in factores  # contribuição zero omitida


def test_decisao_sem_fatores() -> None:
    decision = Decision(
        applicant_id="C-2", score=600, outcome=DecisionOutcome.APPROVED,
        reason_codes=[],
    )
    expl = ExplanationGenerator().explain_decision(decision)
    assert "600" in expl.text
    assert expl.supporting_facts == []


# --------------------------------------------------------------------------- #
# Verificação de factos (deteção de alucinações)
# --------------------------------------------------------------------------- #
def test_explicacao_correta_verifica() -> None:
    expl = ExplanationGenerator().explain_decision(_decision())
    result = FactChecker().check(expl)
    assert result.verified is True
    assert result.issues == []


def test_deteta_score_falso() -> None:
    expl = ExplanationGenerator().explain_decision(_decision())
    # Adultera o score no texto.
    falsa = expl.model_copy(update={"text": expl.text.replace("560", "999")})
    result = FactChecker().check(falsa)
    assert result.verified is False
    assert any("999" in i for i in result.issues)


def test_deteta_contribuicao_falsa() -> None:
    expl = _explanation_with_text(
        "O pedido C-1 foi recusado, com um score de 560. "
        "Os fatores foram: (1) incidentes, contribuição de +15 pontos."
    )
    result = FactChecker().check(expl)
    # +15 não corresponde a nenhum facto real (70, 60, -30).
    assert result.verified is False


def test_explicacao_sem_numeros_verifica() -> None:
    expl = _explanation_with_text("Explicação genérica sem números.")
    result = FactChecker().check(expl)
    assert result.verified is True


# --------------------------------------------------------------------------- #
# Self-consistency
# --------------------------------------------------------------------------- #
def test_consistency_concordante() -> None:
    e1 = ExplanationGenerator().explain_decision(_decision())
    e2 = ExplanationGenerator().explain_decision(_decision())
    result = FactChecker().check_consistency([e1, e2])
    assert result.verified is True


def test_consistency_divergente() -> None:
    e1 = ExplanationGenerator().explain_decision(_decision())
    e2 = e1.model_copy(update={"score": 999})
    result = FactChecker().check_consistency([e1, e2])
    assert result.verified is False


# --------------------------------------------------------------------------- #
# Refinador (fluência opcional com salvaguarda de factos)
# --------------------------------------------------------------------------- #
def test_noop_refiner_mantem_texto() -> None:
    expl = ExplanationGenerator().explain_decision(_decision())
    refined = NoOpRefiner().refine(expl)
    assert refined.text == expl.text


def test_refiner_rejeita_parafrase_com_alucinacao() -> None:
    # Um refinador que corrompe os números deve ser rejeitado, mantendo o
    # texto original (fail-safe).
    class BadRefiner(LLMRefiner):
        def _paraphrase(self, text: str) -> str:
            return text.replace("560", "123")  # introduz facto falso

    expl = ExplanationGenerator().explain_decision(_decision())
    refined = BadRefiner().refine(expl, attempts=3)
    # Como todas as paráfrases falham a verificação, mantém o original.
    assert refined.text == expl.text
    assert "123" not in refined.text


def _explanation_with_text(text: str) -> NaturalExplanation:
    """Ajuda: cria uma explicação com um texto dado e os factos padrão."""
    return NaturalExplanation(
        applicant_id="C-1", text=text, score=560, outcome="recusado",
        supporting_facts=[
            SupportingFact(factor="rendimento_mensal", contribution=70),
            SupportingFact(factor="incidentes", contribution=60),
            SupportingFact(factor="dsti", contribution=-30),
        ],
    )
