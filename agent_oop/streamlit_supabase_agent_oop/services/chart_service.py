import pandas as pd
import plotly.express as px


class ChartService:
    def build_chart(self, data: pd.DataFrame, chart_type: str = "bar"):
        if data is None or data.empty or len(data.columns) < 2:
            return None

        x_col = data.columns[0]
        numeric_cols = data.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            return None

        y_col = numeric_cols[0]

        if chart_type == "line":
            return px.line(data, x=x_col, y=y_col, markers=True)

        return px.bar(data, x=x_col, y=y_col, text_auto=True)
