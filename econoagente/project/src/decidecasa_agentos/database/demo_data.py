from __future__ import annotations

import pandas as pd


def get_demo_data(query_id: str) -> pd.DataFrame:
    examples = {
        "inventory_by_project": pd.DataFrame({
            "proyecto": ["Sialia", "Matera", "Torre Nápoles", "Modena", "Fenix"],
            "unidades_disponibles": [42, 31, 25, 18, 12],
        }),
        "avg_price_m2_by_district": pd.DataFrame({
            "distrito": ["Miraflores", "San Isidro", "Jesús María", "Lince", "Pueblo Libre"],
            "precio_m2_promedio": [11200, 10850, 8350, 7900, 7600],
            "n_unidades": [65, 41, 88, 52, 47],
        }),
        "collections_by_project": pd.DataFrame({
            "proyecto": ["Sialia", "Matera", "Modena", "Fenix"],
            "venta_total": [24000000, 18000000, 12000000, 9000000],
            "cobrado_total": [15000000, 7600000, 9100000, 3200000],
            "pendiente_total": [9000000, 10400000, 2900000, 5800000],
            "porcentaje_cobrado": [0.625, 0.4222, 0.7583, 0.3556],
        }),
        "data_freshness_projects": pd.DataFrame({
            "proyecto": ["Proyecto A", "Proyecto B", "Proyecto C"],
            "url": ["https://example.com/a", "https://example.com/b", "https://example.com/c"],
            "last_seen_at": ["2026-05-01", "2026-05-09", "2026-05-17"],
            "updated_at": ["2026-05-02", "2026-05-10", "2026-05-17"],
            "n_snapshots": [1, 3, 8],
        }),
        "project_metrics_summary": pd.DataFrame({
            "proyecto": ["Sialia", "Matera", "Torre Nápoles"],
            "n_tipologias": [8, 6, 5],
            "sum_unidades_disponibles": [42, 31, 25],
            "min_precio": [310000, 280000, 360000],
            "avg_precio": [525000, 480000, 610000],
            "max_precio": [890000, 760000, 980000],
            "avg_precio_m2": [8200, 7900, 9100],
            "last_seen_at": ["2026-05-18", "2026-05-17", "2026-05-16"],
        }),
    }
    return examples.get(query_id, pd.DataFrame())
