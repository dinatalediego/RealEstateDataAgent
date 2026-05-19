from __future__ import annotations

import pandas as pd

from decidecasa_agentos.core.models import QueryDefinition
from decidecasa_agentos.quality.data_trust_meter import TrustResult


class ExecutiveInsightBuilder:
    """Convierte un DataFrame en respuesta ejecutiva simple."""

    def build(self, question: str, query: QueryDefinition, data: pd.DataFrame, trust: TrustResult) -> str:
        if data is None or data.empty:
            return "No encontré registros para responder con la consulta autorizada seleccionada."

        rows = len(data)
        cols = len(data.columns)
        top_line = self._top_line(query, data)
        return (
            f"**{query.title}.** {top_line}\n\n"
            f"Se analizaron **{rows} filas** y **{cols} columnas** con confianza **{trust.label}**. "
            f"La consulta usada pertenece a **{query.agent}** y está dentro del catálogo autorizado."
        )

    def _top_line(self, query: QueryDefinition, data: pd.DataFrame) -> str:
        if data.empty:
            return "Sin datos disponibles."
        first = data.iloc[0].to_dict()
        if query.id == "inventory_by_project" and "proyecto" in first:
            return f"El mayor stock aparece en **{first.get('proyecto')}** con **{first.get('unidades_disponibles')} unidades disponibles**."
        if query.id == "avg_price_m2_by_district" and "distrito" in first:
            return f"El distrito con mayor precio m2 promedio es **{first.get('distrito')}** con **S/ {first.get('precio_m2_promedio')}**."
        if query.id == "collections_by_project" and "proyecto" in first:
            return f"El mayor pendiente está en **{first.get('proyecto')}** con **S/ {first.get('pendiente_total'):,.0f}** por cobrar."
        if query.id == "data_freshness_projects" and "proyecto" in first:
            return f"El proyecto más antiguo según orden de frescura es **{first.get('proyecto')}**."
        return "Resultado disponible para revisión en tabla y gráfico."
