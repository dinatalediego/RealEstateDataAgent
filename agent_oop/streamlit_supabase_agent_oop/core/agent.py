from dataclasses import dataclass
from typing import Any, Dict

from core.intent_router import IntentRouter
from core.response_builder import ResponseBuilder
from core.session_memory import SessionMemory
from database.query_registry import QueryRegistry
from services.query_executor import QueryExecutor


@dataclass
class AgentResult:
    answer: str
    data: Any = None
    sql: str | None = None
    query_key: str | None = None
    chart_type: str | None = None
    error: str | None = None


class StreamlitSupabaseAgent:
    def __init__(
        self,
        registry: QueryRegistry,
        router: IntentRouter,
        executor: QueryExecutor,
        response_builder: ResponseBuilder,
        memory: SessionMemory,
    ):
        self.registry = registry
        self.router = router
        self.executor = executor
        self.response_builder = response_builder
        self.memory = memory

    def answer(self, question: str) -> AgentResult:
        query = self.router.route(question)

        if query is None:
            self.memory.add(question, None, "not_matched")
            return AgentResult(
                answer=(
                    "Todavía no tengo una consulta autorizada para esa pregunta. "
                    "Prueba con inventario, precio m2, cobranzas, asesores, compradores o calidad de datos."
                ),
                error="Pregunta sin intención autorizada.",
            )

        try:
            data = self.executor.run(query.sql)
            answer = self.response_builder.build(question, query, data)
            self.memory.add(question, query.key, "success")
            return AgentResult(
                answer=answer,
                data=data,
                sql=query.sql,
                query_key=query.key,
                chart_type=query.chart_type,
            )
        except Exception as exc:
            self.memory.add(question, query.key, "error")
            return AgentResult(
                answer="No pude ejecutar la consulta. Revisa conexión, nombres de tablas o permisos.",
                sql=query.sql,
                query_key=query.key,
                error=str(exc),
            )
