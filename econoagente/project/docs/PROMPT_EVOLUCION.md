# Prompt para evolucionar este proyecto en otra consulta

Quiero evolucionar mi proyecto `DecideCasa AgentOS`, una app Streamlit conectada a Supabase/Postgres para responder preguntas inmobiliarias con arquitectura OOP.

La estructura actual tiene:

- `app.py`
- `config/query_catalog.yaml`
- `src/decidecasa_agentos/core/agent.py`
- `src/decidecasa_agentos/core/questions.py`
- `src/decidecasa_agentos/catalog/query_catalog.py`
- `src/decidecasa_agentos/security/query_shield.py`
- `src/decidecasa_agentos/database/supabase_runner.py`
- `src/decidecasa_agentos/quality/data_trust_meter.py`
- `src/decidecasa_agentos/insights/executive_insight_builder.py`
- `src/decidecasa_agentos/visualization/insight_chart_builder.py`
- `src/decidecasa_agentos/audit/query_audit_trail.py`

Quiero que mejores el proyecto hacia una versión PRO con:

1. Agentes especializados:
   - CommercialAgent
   - InventoryAgent
   - FinanceAgent
   - DataQualityAgent
   - GeoAgent
   - MarketAgent

2. Filtros dinámicos:
   - proyecto
   - distrito
   - fuente
   - rango de fechas

3. Auditoría persistente en Supabase.

4. Catálogo de preguntas más completo.

5. Modo de exportación a Excel.

6. Mejor UI ejecutiva con KPIs, tabs y estado de confianza.

7. Seguridad reforzada:
   - usuario read-only
   - schemas permitidos
   - tablas permitidas
   - timeout
   - max rows
   - bloqueo de SQL peligroso

Generar código end-to-end manteniendo compatibilidad con Streamlit Cloud.
