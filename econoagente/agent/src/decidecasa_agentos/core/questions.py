from __future__ import annotations

import re

from decidecasa_agentos.catalog.query_catalog import BusinessQuestionCatalog
from decidecasa_agentos.core.models import QueryDefinition


class QuestionNormalizer:
    def normalize(self, question: str) -> str:
        text = question.lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text


class BusinessVocabulary:
    """Sinónimos de negocio para mejorar el match sin usar LLM."""

    synonyms = {
        "depas": "unidades departamentos inventario stock",
        "depa": "unidad departamento inventario stock",
        "por vender": "disponible disponibilidad stock",
        "m2": "precio m2 precio por m2 metro cuadrado",
        "plata": "cobranza pagos cobrado pendiente",
        "scrapeo": "scraping last_seen_at updated_at frescura",
    }

    def expand(self, question: str) -> str:
        enriched = question
        for word, expansion in self.synonyms.items():
            if word in question:
                enriched += " " + expansion
        return enriched


class BusinessQuestionRouter:
    """Decide qué consulta aprobada responde mejor la pregunta."""

    def __init__(self, catalog: BusinessQuestionCatalog) -> None:
        self.catalog = catalog
        self.normalizer = QuestionNormalizer()
        self.vocabulary = BusinessVocabulary()

    def route(self, question: str) -> QueryDefinition | None:
        normalized = self.normalizer.normalize(question)
        enriched = self.vocabulary.expand(normalized)

        best_query = None
        best_score = 0
        for query in self.catalog.list_queries():
            score = sum(1 for kw in query.keywords if kw.lower() in enriched)
            if score > best_score:
                best_query = query
                best_score = score
        return best_query
