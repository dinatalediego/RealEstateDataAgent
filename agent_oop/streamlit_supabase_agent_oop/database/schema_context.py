from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class TableContext:
    table_name: str
    business_name: str
    description: str
    key_columns: List[str]
    metric_columns: List[str]


class SchemaContext:
    """
    Diccionario de datos mínimo para que el agente no responda a ciegas.
    Adaptar estos nombres a tus tablas reales en Supabase.
    """

    def __init__(self):
        self.tables: Dict[str, TableContext] = {
            "inventory": TableContext(
                table_name="gold.fact_inventory",
                business_name="Inventario inmobiliario",
                description="Unidades, proyectos, estados comerciales, precios y tipologías.",
                key_columns=["proyecto", "distrito", "tipo_unidad", "estado_comercial"],
                metric_columns=["precio", "area", "precio_m2"],
            ),
            "cobranzas": TableContext(
                table_name="gold.fact_cobranzas",
                business_name="Cobranzas y pagos",
                description="Ventas, montos cobrados, pendientes y avance de cobranza.",
                key_columns=["proyecto", "cliente", "documento_cliente"],
                metric_columns=["monto_venta", "monto_cobrado", "monto_pendiente"],
            ),
            "sales": TableContext(
                table_name="gold.fact_sales",
                business_name="Ventas y separaciones",
                description="Separaciones, minutas, asesores, medios de captación y fechas comerciales.",
                key_columns=["proyecto", "asesor", "medio_captacion", "periodo"],
                metric_columns=["monto_venta", "cantidad_ventas", "cantidad_separaciones"],
            ),
            "quality": TableContext(
                table_name="gold.fact_data_quality",
                business_name="Calidad de datos",
                description="Inconsistencias, duplicados, campos faltantes y cruces fallidos.",
                key_columns=["proyecto", "tipo_error", "severidad"],
                metric_columns=["n_registros", "porcentaje_error"],
            ),
        }

    def describe(self) -> str:
        lines = []
        for key, table in self.tables.items():
            lines.append(f"{key}: {table.table_name} — {table.description}")
        return "\n".join(lines)
