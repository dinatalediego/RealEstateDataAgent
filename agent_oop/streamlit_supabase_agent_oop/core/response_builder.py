import pandas as pd
from database.query_registry import QueryDefinition


class ResponseBuilder:
    def build(self, question: str, query: QueryDefinition, data: pd.DataFrame) -> str:
        if data is None or data.empty:
            return (
                f"No encontré resultados para responder: '{question}'. "
                "Puede deberse a filtros, nombres de tablas o falta de datos."
            )

        rows = len(data)
        cols = len(data.columns)

        numeric_cols = data.select_dtypes(include="number").columns.tolist()
        first_metric = numeric_cols[0] if numeric_cols else None

        metric_text = ""
        if first_metric:
            total_value = data[first_metric].sum()
            metric_text = f" La métrica principal suma aproximadamente **{total_value:,.2f}**."

        return (
            f"✅ Respondí usando **{query.title}** del área **{query.area}**. "
            f"La consulta devolvió **{rows} filas** y **{cols} columnas**.{metric_text} "
            "Revisa la tabla y el gráfico para detectar prioridades de acción."
        )
