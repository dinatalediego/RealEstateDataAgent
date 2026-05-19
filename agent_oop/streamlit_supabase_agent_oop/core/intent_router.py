from typing import Optional
from database.query_registry import QueryRegistry, QueryDefinition


class IntentRouter:
    """
    Decide qué consulta autorizada responde mejor a la pregunta.
    Versión 1: keywords.
    Versión futura: embeddings + catálogo + permisos por usuario.
    """

    def __init__(self, registry: QueryRegistry):
        self.registry = registry

    def route(self, question: str) -> Optional[QueryDefinition]:
        return self.registry.match(question)
