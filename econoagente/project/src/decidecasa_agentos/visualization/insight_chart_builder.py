from __future__ import annotations

import altair as alt
import pandas as pd

from decidecasa_agentos.core.models import QueryDefinition


class InsightChartBuilder:
    def build(self, query: QueryDefinition, data: pd.DataFrame):
        if data is None or data.empty or query.chart == "table":
            return None
        numeric_cols = list(data.select_dtypes(include="number").columns)
        text_cols = [c for c in data.columns if c not in numeric_cols]
        if not numeric_cols or not text_cols:
            return None
        x_col = text_cols[0]
        y_col = numeric_cols[0]
        return alt.Chart(data).mark_bar().encode(
            x=alt.X(f"{x_col}:N", sort="-y", title=x_col),
            y=alt.Y(f"{y_col}:Q", title=y_col),
            tooltip=list(data.columns),
        ).properties(height=380)
