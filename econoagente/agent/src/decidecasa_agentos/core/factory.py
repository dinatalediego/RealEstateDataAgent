from __future__ import annotations

from decidecasa_agentos.audit.query_audit_trail import QueryAuditTrail
from decidecasa_agentos.catalog.query_catalog import BusinessQuestionCatalog
from decidecasa_agentos.core.agent import AgentCouncil, RealEstateDataAgent
from decidecasa_agentos.core.models import AgentProfile
from decidecasa_agentos.core.questions import BusinessQuestionRouter
from decidecasa_agentos.database.supabase_runner import SupabaseQueryRunner
from decidecasa_agentos.insights.executive_insight_builder import ExecutiveInsightBuilder
from decidecasa_agentos.quality.data_trust_meter import DataTrustMeter
from decidecasa_agentos.security.query_shield import QueryShield
from decidecasa_agentos.utils.settings import AppSettings


def build_agent_council(settings: AppSettings) -> AgentCouncil:
    catalog = BusinessQuestionCatalog()
    router = BusinessQuestionRouter(catalog)
    shield = QueryShield(settings.allowed_schemas, max_rows=settings.max_rows)
    runner = SupabaseQueryRunner(settings)
    trust_meter = DataTrustMeter()
    insight_builder = ExecutiveInsightBuilder()
    audit_trail = QueryAuditTrail(settings.log_path)

    agent = RealEstateDataAgent(
        profile=AgentProfile(),
        catalog=catalog,
        router=router,
        shield=shield,
        runner=runner,
        trust_meter=trust_meter,
        insight_builder=insight_builder,
        audit_trail=audit_trail,
    )
    return AgentCouncil(agent)
