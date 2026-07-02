"""Demonstração isolada dos módulos CREDERE: Compliance e Explicação.

Esta demo mostra os dois módulos-estrela do CREDERE de forma autónoma, usando um
dicionário de dados que SIMULA o output da camada de Machine Learning (score,
probabilidade e variáveis do candidato). Não precisa do pipeline completo.

Mostra:
  1. O motor de explicação a gerar uma justificação em português.
  2. O motor de compliance a VETAR uma decisão quando uma regra dura é violada.

Correr:
    python run_demo_isolated.py
"""

from __future__ import annotations

import logging

logging.disable(logging.CRITICAL)

from credere.compliance import ComplianceGate
from credere.explanation import ExplanationGenerator, FactChecker
from credere.scoring.models import (
    CreditApplication,
    Decision,
    DecisionOutcome,
    ReasonCode,
)


def _linha(char: str = "─", n: int = 64) -> None:
    print(char * n)


# --------------------------------------------------------------------------- #
# DADOS MOCK: simulam o output que viria da camada de Machine Learning.
# Altere estes valores para ver o comportamento dos módulos mudar.
# --------------------------------------------------------------------------- #
CANDIDATO_APROVAVEL = {
    "applicant_id": "DEMO-APROVA",
    "score": 720,
    "outcome": DecisionOutcome.APPROVED,
    "attributes": {"rendimento_mensal": 3200, "dsti": 25, "incidentes": 0},
    "reason_codes": [
        ("rendimento_mensal", 70, "alto"),
        ("incidentes", 40, "sem incidentes"),
        ("dsti", 20, "moderado"),
    ],
}

# Este candidato tem DSTI de 60% — acima do limite legal de 40%.
# O modelo "aprovou" (score alto), mas o compliance vai VETAR.
CANDIDATO_VETO = {
    "applicant_id": "DEMO-VETO",
    "score": 700,
    "outcome": DecisionOutcome.APPROVED,
    "attributes": {"rendimento_mensal": 3000, "dsti": 60, "incidentes": 0},
    "reason_codes": [
        ("rendimento_mensal", 60, "alto"),
        ("dsti", -30, "crítico"),
    ],
}


def _build_decision(mock: dict) -> tuple[Decision, CreditApplication]:
    """Constrói a decisão e a candidatura a partir do dicionário mock."""
    decision = Decision(
        applicant_id=mock["applicant_id"],
        score=mock["score"],
        outcome=mock["outcome"],
        reason_codes=[
            ReasonCode(factor=f, points=p, band_label=b)
            for f, p, b in mock["reason_codes"]
        ],
    )
    application = CreditApplication(
        applicant_id=mock["applicant_id"], attributes=mock["attributes"]
    )
    return decision, application


def demo_explicacao(mock: dict) -> None:
    """Mostra o motor de explicação a gerar uma justificação em português."""
    decision, _ = _build_decision(mock)
    explanation = ExplanationGenerator().explain_decision(decision)

    print("\n1. MOTOR DE EXPLICAÇÃO (determinístico, exato ao número)\n")
    print("   " + explanation.text.replace(". ", ".\n   "))

    # Verificação de factos: prova que a explicação não tem alucinações.
    result = FactChecker().check(explanation)
    print(f"\n   Verificação de factos: "
          f"{'APROVADA' if result.verified else 'FALHOU'} "
          f"({result.checked_values} valores conferidos contra os dados)")


def demo_compliance(mock: dict) -> None:
    """Mostra o motor de compliance a aplicar (ou não) um veto."""
    decision, application = _build_decision(mock)
    verdict = ComplianceGate().evaluate(application, decision)

    print("\n2. MOTOR DE COMPLIANCE (neuro-simbólico, com poder de veto)\n")
    print(f"   Decisão do modelo estatístico: {verdict.original_outcome}")
    print(f"   Decisão final após compliance:  {verdict.final_outcome}")
    print(f"   Vetado: {'SIM' if verdict.vetoed else 'não'}")
    if verdict.alerts:
        print("\n   Alertas:")
        for alerta in verdict.alerts:
            print(f"   • {alerta}")


def main() -> None:
    """Corre a demonstração isolada."""
    print("\n")
    _linha("═")
    print("  CREDERE — Demonstração Isolada: Compliance + Explicação")
    _linha("═")
    print("\nOs dados abaixo SIMULAM o output da camada de Machine Learning.")
    print("Edite CANDIDATO_APROVAVEL / CANDIDATO_VETO no ficheiro para "
          "experimentar.")

    # Caso 1: candidato aprovável — explicação limpa, sem veto.
    _linha()
    print("CASO 1 — Candidato aprovável (DSTI 25%, sem incidentes)")
    _linha()
    demo_explicacao(CANDIDATO_APROVAVEL)
    demo_compliance(CANDIDATO_APROVAVEL)

    # Caso 2: o modelo aprova, mas a taxa de esforço viola a lei → VETO.
    print("\n")
    _linha()
    print("CASO 2 — O modelo aprova, mas DSTI de 60% viola o limite legal")
    _linha()
    demo_explicacao(CANDIDATO_VETO)
    demo_compliance(CANDIDATO_VETO)

    print("\n")
    _linha("═")
    print("  Repare: no Caso 2, a regra legal VETOU a decisão do modelo.")
    print("  O simbólico tem primazia sobre o estatístico — é isto que torna")
    print("  o sistema defensável perante regulação de alto risco.")
    _linha("═")
    print()


if __name__ == "__main__":
    main()
