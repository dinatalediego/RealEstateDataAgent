from __future__ import annotations

from pathlib import Path

import yaml

from decidecasa_agentos.core.models import QueryDefinition


class BusinessQuestionCatalog:
    """Biblioteca de preguntas autorizadas y SQL aprobado."""

    def __init__(self, catalog_path: str | Path = "config/query_catalog.yaml") -> None:
        self.catalog_path = Path(catalog_path)
        self.queries = self._load_queries()

    def _load_queries(self) -> list[QueryDefinition]:
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"No existe el catálogo: {self.catalog_path}")
        payload = yaml.safe_load(self.catalog_path.read_text(encoding="utf-8")) or {}
        return [QueryDefinition(**item) for item in payload.get("queries", [])]

    def list_queries(self) -> list[QueryDefinition]:
        return self.queries

    def get_by_id(self, query_id: str) -> QueryDefinition | None:
        return next((q for q in self.queries if q.id == query_id), None)
