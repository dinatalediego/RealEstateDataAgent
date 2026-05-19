from __future__ import annotations

from decidecasa_agentos.audit.query_audit_trail import QueryAuditTrail
from decidecasa_agentos.catalog.query_catalog import BusinessQuestionCatalog
from decidecasa_agentos.core.models import AgentProfile, AgentResponse
from decidecasa_agentos.core.questions import BusinessQuestionRouter
from decidecasa_agentos.database.supabase_runner import SupabaseQueryRunner
from decidecasa_agentos.insights.executive_insight_builder import ExecutiveInsightBuilder
from decidecasa_agentos.quality.data_trust_meter import DataTrustMeter
from decidecasa_agentos.security.query_shield import QueryShield


class RealEstateDataAgent:
    """Pregunta -> router -> SQL aprobado -> QueryShield -> Supabase -> confianza -> insight."""

    def __init__(
        self,
        profile: AgentProfile,
        catalog: BusinessQuestionCatalog,
        router: BusinessQuestionRouter,
        shield: QueryShield,
        runner: SupabaseQueryRunner,
        trust_meter: DataTrustMeter,
        insight_builder: ExecutiveInsightBuilder,
        audit_trail: QueryAuditTrail,
    ) -> None:
        self.profile = profile
        self.catalog = catalog
        self.router = router
        self.shield = shield
        self.runner = runner
        self.trust_meter = trust_meter
        self.insight_builder = insight_builder
        self.audit_trail = audit_trail

    def answer(self, question: str, forced_query_id: str | None = None) -> AgentResponse:
        query = self.catalog.get_by_id(forced_query_id) if forced_query_id else self.router.route(question)
        if query is None:
            response = AgentResponse(
                question=question,
                query=None,
                answer=(
                    "No encontré una consulta autorizada para esa pregunta. "
                    "Prueba con stock, precio m2, cobranzas, frescura de scraping o métricas por proyecto."
                ),
                warnings=["Pregunta fuera del catálogo autorizado."],
                confidence_label="No aplica",
            )
            self.audit_trail.record(response, status="no_match")
            return response

        shield_result = self.shield.validate(query.sql)
        if not shield_result.allowed:
            response = AgentResponse(
                question=question,
                query=query,
                answer=f"Consulta bloqueada por seguridad: {shield_result.reason}",
                warnings=[shield_result.reason or "Bloqueada por QueryShield"],
                confidence_label="Bloqueada 🛡️",
            )
            self.audit_trail.record(response, status="blocked")
            return response

        try:
            data = self.runner.run(query, shield_result.sql or query.sql)
            critical = query.confidence_rules.get("critical_columns", []) if query.confidence_rules else []
            trust = self.trust_meter.score(data, critical_columns=critical)
            answer = self.insight_builder.build(question, query, data, trust)
            response = AgentResponse(
                question=question,
                query=query,
                answer=answer,
                data=data,
                sql=shield_result.sql,
                confidence_label=trust.label,
                confidence_score=trust.score,
                warnings=trust.warnings,
            )
            self.audit_trail.record(response, status="ok")
            return response
        except Exception as exc:  # noqa: BLE001
            response = AgentResponse(
                question=question,
                query=query,
                answer=f"Ocurrió un error ejecutando la consulta: {exc}",
                sql=shield_result.sql,
                warnings=[str(exc)],
                confidence_label="Error 🔴",
            )
            self.audit_trail.record(response, status="error")
            return response


class AgentCouncil:
    """Organización de agentes. En esta v1 coordina un agente principal extensible."""

    def __init__(self, main_agent: RealEstateDataAgent) -> None:
        self.main_agent = main_agent

    def ask(self, question: str, forced_query_id: str | None = None) -> AgentResponse:
        return self.main_agent.answer(question=question, forced_query_id=forced_query_id)
