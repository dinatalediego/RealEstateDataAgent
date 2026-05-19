# 🧠 Streamlit Supabase Agent OOP

Aplicación web en **Streamlit** para consultar una base de datos en **Supabase/Postgres** usando una arquitectura OOP, segura y extensible.

La idea central:

> Streamlit es la interfaz.  
> OOP es la mente.  
> Supabase es la fuente.  
> El agente es el analista que responde con reglas.

---

## ✅ Qué incluye

- App web con Streamlit.
- Arquitectura OOP modular.
- Conexión a Supabase vía `SUPABASE_DATABASE_URL`.
- Catálogo seguro de preguntas autorizadas.
- Motor de intención por keywords.
- Validación SQL defensiva.
- Respuestas ejecutivas con tabla, métricas y gráfico automático.
- Historial de preguntas.
- `.env.example` listo para GitHub.
- Guía de despliegue.
- Checklist de seguridad y mejoras.

---

## 📁 Estructura

```text
streamlit_supabase_agent_oop/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── config/
│   └── settings.py
│
├── core/
│   ├── agent.py
│   ├── intent_router.py
│   ├── response_builder.py
│   ├── safety.py
│   └── session_memory.py
│
├── database/
│   ├── query_registry.py
│   ├── schema_context.py
│   └── supabase_connection.py
│
├── services/
│   ├── chart_service.py
│   └── query_executor.py
│
├── ui/
│   ├── layout.py
│   └── sidebar.py
│
├── docs/
│   ├── 01_que_no_estabas_considerando.md
│   ├── 02_github_deploy.md
│   └── 03_prompt_para_evolucionar.md
│
└── examples/
    └── preguntas_clave.md
```

---

## 🚀 Instalación local

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

En Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

---

## 🔐 Variables de entorno

Editar `.env`:

```env
SUPABASE_DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:5432/postgres
APP_ENV=local
MAX_ROWS=500
```

No subir `.env` a GitHub.

---

## 🧩 Filosofía del agente

Primera versión recomendada:

```text
Pregunta natural → intención detectada → SQL autorizado → Supabase → tabla/gráfico/insight
```

No se recomienda empezar con SQL libre generado por IA. Primero conviene usar un **catálogo controlado de preguntas clave**.

---

## 🧠 Ejemplos de preguntas

- ¿Cuántas unidades disponibles hay por proyecto?
- ¿Cuál es el precio promedio por m2 por distrito?
- ¿Cuánto se ha cobrado por proyecto?
- ¿Qué proyectos tienen mayor brecha de cobranza?
- ¿Qué distritos concentran más compradores?
- ¿Qué ventas no tienen documento de cliente?

---

## ⚠️ Importante

Este proyecto trae SQL de ejemplo con nombres genéricos como:

- `gold.fact_inventory`
- `gold.fact_cobranzas`
- `gold.fact_sales`
- `gold.fact_unit_metrics`

Debes adaptar esos nombres a tus tablas reales de Supabase.

---

## 🏆 Próxima evolución

1. Login por usuario.
2. Roles por área: Comercial, Finanzas, Calidad, Geo.
3. Registro de preguntas frecuentes.
4. RAG con diccionario de datos.
5. SQL generado por IA, pero validado contra permisos y solo lectura.
6. Deploy con Streamlit Community Cloud, Render o Railway.
