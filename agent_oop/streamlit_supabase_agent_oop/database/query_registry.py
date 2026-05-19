from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class QueryDefinition:
    key: str
    area: str
    title: str
    description: str
    keywords: List[str]
    sql: str
    chart_type: str = "bar"


class QueryRegistry:
    """
    Catálogo de consultas autorizadas.
    Esta capa evita que el agente ejecute SQL libre sin control.
    """

    def __init__(self):
        self.queries: Dict[str, QueryDefinition] = {
            "inventory_by_project": QueryDefinition(
                key="inventory_by_project",
                area="Inventario",
                title="Unidades disponibles por proyecto",
                description="Cuenta unidades disponibles agrupadas por proyecto.",
                keywords=["disponibilidad", "disponibles", "stock", "inventario", "unidades por vender"],
                sql="""
                    select
                        proyecto,
                        count(*) as unidades_disponibles
                    from gold.fact_inventory
                    where lower(coalesce(estado_comercial, '')) in ('disponible', 'por vender', '02_por vender')
                    group by proyecto
                    order by unidades_disponibles desc
                """,
                chart_type="bar",
            ),
            "price_m2_by_district": QueryDefinition(
                key="price_m2_by_district",
                area="Mercado / Inventario",
                title="Precio promedio por m2 por distrito",
                description="Calcula el precio m2 promedio por distrito.",
                keywords=["precio m2", "precio por m2", "metro cuadrado", "distrito", "precio promedio"],
                sql="""
                    select
                        distrito,
                        round(avg(precio_m2)::numeric, 2) as precio_m2_promedio
                    from gold.fact_unit_metrics
                    where precio_m2 is not null
                    group by distrito
                    order by precio_m2_promedio desc
                """,
                chart_type="bar",
            ),
            "collections_by_project": QueryDefinition(
                key="collections_by_project",
                area="Finanzas",
                title="Cobranzas por proyecto",
                description="Resume venta, cobrado, pendiente y porcentaje cobrado por proyecto.",
                keywords=["cobranza", "cobranzas", "cobrado", "pagos", "pendiente", "brecha"],
                sql="""
                    select
                        proyecto,
                        sum(monto_venta) as venta_total,
                        sum(monto_cobrado) as cobrado_total,
                        sum(monto_pendiente) as pendiente_total,
                        round((sum(monto_cobrado) / nullif(sum(monto_venta), 0))::numeric, 4) as porcentaje_cobrado
                    from gold.fact_cobranzas
                    group by proyecto
                    order by pendiente_total desc
                """,
                chart_type="bar",
            ),
            "sales_by_advisor": QueryDefinition(
                key="sales_by_advisor",
                area="Comercial",
                title="Ranking de asesores por ventas",
                description="Ranking comercial por asesor.",
                keywords=["asesor", "ranking asesor", "vendedor", "ventas por asesor", "separaciones por asesor"],
                sql="""
                    select
                        asesor,
                        count(*) as cantidad_ventas,
                        sum(monto_venta) as monto_venta_total
                    from gold.fact_sales
                    where asesor is not null
                    group by asesor
                    order by cantidad_ventas desc, monto_venta_total desc
                """,
                chart_type="bar",
            ),
            "data_quality_issues": QueryDefinition(
                key="data_quality_issues",
                area="Calidad de datos",
                title="Problemas de calidad de datos",
                description="Lista inconsistencias agrupadas por tipo de error.",
                keywords=["calidad", "errores", "duplicados", "nulos", "inconsistencias", "contrato", "documento"],
                sql="""
                    select
                        tipo_error,
                        severidad,
                        count(*) as n_registros
                    from gold.fact_data_quality
                    group by tipo_error, severidad
                    order by n_registros desc
                """,
                chart_type="bar",
            ),
            "buyers_by_district": QueryDefinition(
                key="buyers_by_district",
                area="Cliente / Geo",
                title="Compradores por distrito",
                description="Ranking de distritos de procedencia de compradores.",
                keywords=["compradores", "distrito compradores", "procedencia", "clientes por distrito", "ranking distritos"],
                sql="""
                    select
                        distrito_cliente,
                        count(distinct documento_cliente) as compradores
                    from gold.fact_sales
                    where distrito_cliente is not null
                    group by distrito_cliente
                    order by compradores desc
                """,
                chart_type="bar",
            ),
        }

    def all(self) -> List[QueryDefinition]:
        return list(self.queries.values())

    def get(self, key: str) -> Optional[QueryDefinition]:
        return self.queries.get(key)

    def match(self, question: str) -> Optional[QueryDefinition]:
        text = question.lower().strip()
        best_query = None
        best_score = 0

        for query in self.queries.values():
            score = sum(1 for kw in query.keywords if kw.lower() in text)
            if score > best_score:
                best_score = score
                best_query = query

        return best_query
