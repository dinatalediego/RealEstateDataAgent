# 🧠 DecideCasa AgentOS — Streamlit + Supabase + OOP

Aplicación end-to-end para consultar una base inmobiliaria en Supabase usando una organización de clases OOP:

- `RealEstateDataAgent`: agente principal.
- `AgentCouncil`: coordinación de agentes.
- `BusinessQuestionRouter`: entiende preguntas.
- `BusinessQuestionCatalog`: catálogo seguro de preguntas autorizadas.
- `QueryShield`: seguridad SQL.
- `SupabaseQueryRunner`: conexión a Supabase/Postgres.
- `DataTrustMeter`: confianza/calidad de respuesta.
- `ExecutiveInsightBuilder`: narrativa ejecutiva.
- `InsightChartBuilder`: gráfico automático.
- `QueryAuditTrail`: trazabilidad local.

## 1. Probar localmente en modo demo

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
streamlit run app.py
```

En modo demo no necesitas Supabase. Usa data simulada.

## 2. Conectar Supabase

Copia `.env.example` como `.env`:

```bash
cp .env.example .env
```

Edita:

```env
APP_MODE=production
SUPABASE_DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require
AGENT_ALLOWED_SCHEMAS=gold,mart,public
AGENT_MAX_ROWS=500
```

Luego:

```bash
streamlit run app.py
```

## 3. Personalizar preguntas

Edita:

```text
config/query_catalog.yaml
```

Cada pregunta tiene:

- `id`
- `agent`
- `title`
- `keywords`
- `sql`
- `chart`
- `confidence_rules`

Regla: empieza con SQL autorizado y probado en Supabase.

## 4. Seguridad incluida

`QueryShield` bloquea operaciones peligrosas:

- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `TRUNCATE`
- `ALTER`
- `CREATE`
- `GRANT`
- `REVOKE`

También valida esquemas permitidos y agrega `LIMIT` si falta.

## 5. Estructura

```text
app.py
config/query_catalog.yaml
src/decidecasa_agentos/
  core/
  catalog/
  security/
  database/
  quality/
  insights/
  visualization/
  ui/
  audit/
scripts/
docs/
```

## 6. Deploy recomendado

Ver `docs/DEPLOYMENT_GUIDE.md`.
