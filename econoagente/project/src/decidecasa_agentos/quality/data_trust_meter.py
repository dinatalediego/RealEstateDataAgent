from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TrustResult:
    label: str
    score: float
    warnings: list[str]


class DataTrustMeter:
    """Calcula confianza básica de una respuesta según completitud y filas retornadas."""

    def score(self, data: pd.DataFrame | None, critical_columns: list[str] | None = None) -> TrustResult:
        if data is None or data.empty:
            return TrustResult("Baja 🔴", 0.0, ["La consulta no devolvió registros."])

        warnings: list[str] = []
        score = 1.0

        critical_columns = critical_columns or []
        missing_cols = [c for c in critical_columns if c not in data.columns]
        if missing_cols:
            score -= 0.35
            warnings.append(f"Faltan columnas críticas esperadas: {', '.join(missing_cols)}.")

        available_critical = [c for c in critical_columns if c in data.columns]
        for col in available_critical:
            null_rate = float(data[col].isna().mean())
            if null_rate > 0.2:
                score -= 0.15
                warnings.append(f"La columna {col} tiene {null_rate:.0%} de nulos.")

        if len(data) < 3:
            score -= 0.10
            warnings.append("La muestra tiene pocos registros; interpretar con cuidado.")

        score = max(0.0, min(1.0, score))
        if score >= 0.80:
            label = "Alta 🟢"
        elif score >= 0.50:
            label = "Media 🟡"
        else:
            label = "Baja 🔴"
        return TrustResult(label, score, warnings)
