from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decidecasa_agentos.catalog.query_catalog import BusinessQuestionCatalog
from decidecasa_agentos.core.factory import build_agent_council
from decidecasa_agentos.database.supabase_runner import ConnectionHealthCheck
from decidecasa_agentos.utils.settings import load_settings
from decidecasa_agentos.visualization.insight_chart_builder import InsightChartBuilder

st.set_page_config(
    page_title="DecideCasa AgentOS",
    page_icon="🧠",
    layout="wide",
)

settings = load_settings()
#catalog = BusinessQuestionCatalog()
catalog = BusinessQuestionCatalog(ROOT / "config" / "query_catalog.yaml")
health = ConnectionHealthCheck(settings)
chart_builder = InsightChartBuilder()

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🧠 DecideCasa AgentOS")
st.caption("Organización OOP de agentes para consultar Supabase con seguridad, trazabilidad e insights inmobiliarios.")

with st.sidebar:
    st.header("⚙️ Control del AgentOS")
    ok, msg = health.status()
    # Evitar ternario con comandos Streamlit: Streamlit puede intentar renderizar
    # el DeltaGenerator devuelto por st.success/st.error y lanzar _repr_html_ error.
    if ok:
        st.success(msg)
    else:
        st.error(msg)
    st.write(f"**Modo:** `{settings.app_mode}`")
    st.write(f"**Esquemas permitidos:** `{', '.join(settings.allowed_schemas)}`")
    st.write(f"**Máx. filas:** `{settings.max_rows}`")

    st.divider()
    st.subheader("Preguntas autorizadas")
    query_options = {f"{q.agent} · {q.title}": q.id for q in catalog.list_queries()}
    selected_label = st.selectbox("Forzar una consulta del catálogo", ["Auto-detectar"] + list(query_options.keys()))
    forced_query_id = None if selected_label == "Auto-detectar" else query_options[selected_label]

    st.divider()
    if st.button("Limpiar historial"):
        st.session_state.history = []
        st.rerun()

examples = [
    "¿Cuántas unidades disponibles hay por proyecto?",
    "¿Cuál es el precio promedio por m2 por distrito?",
    "¿Cuánto falta cobrar por proyecto?",
    "¿Qué proyectos están desactualizados por last_seen_at?",
    "Dame un resumen de métricas por proyecto",
]

st.markdown("### Pregunta de negocio")
question = st.text_input(
    "Escribe tu pregunta",
    placeholder="Ejemplo: ¿Qué proyectos tienen más stock disponible?",
)

cols = st.columns(len(examples))
for col, example in zip(cols, examples):
    if col.button(example, use_container_width=True):
        question = example

if st.button("Responder", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Escribe una pregunta o selecciona un ejemplo.")
    else:
        council = build_agent_council(settings)
        response = council.ask(question, forced_query_id=forced_query_id)
        st.session_state.history.insert(0, response)

if st.session_state.history:
    response = st.session_state.history[0]
    st.divider()
    st.markdown("## Resultado")
    st.markdown(response.answer)

    m1, m2, m3 = st.columns(3)
    m1.metric("Confianza", response.confidence_label)
    m2.metric("Filas", 0 if response.data is None else len(response.data))
    m3.metric("Agente", response.query.agent if response.query else "Sin match")

    if response.warnings:
        with st.expander("⚠️ Advertencias de calidad / seguridad", expanded=True):
            for warning in response.warnings:
                st.warning(warning)

    if response.has_data:
        chart = chart_builder.build(response.query, response.data) if response.query else None
        if chart is not None:
            st.altair_chart(chart, use_container_width=True)
        st.dataframe(response.data, use_container_width=True)

    with st.expander("Ver SQL utilizado"):
        if response.sql:
            st.code(response.sql, language="sql")
        else:
            st.info("No se ejecutó SQL para esta respuesta.")

    with st.expander("Historial de sesión"):
        for item in st.session_state.history[:10]:
            st.write(f"- **{item.created_at.strftime('%H:%M:%S')}** · {item.question} · {item.confidence_label}")
else:
    st.info("Haz una pregunta para iniciar. En modo demo no necesitas conectar Supabase.")
