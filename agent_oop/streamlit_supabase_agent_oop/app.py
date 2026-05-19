import streamlit as st

from config.settings import get_settings
from core.agent import StreamlitSupabaseAgent
from core.intent_router import IntentRouter
from core.response_builder import ResponseBuilder
from core.safety import SQLSafetyGuard
from core.session_memory import SessionMemory
from database.query_registry import QueryRegistry
from database.supabase_connection import SupabasePostgresConnection
from services.chart_service import ChartService
from services.query_executor import QueryExecutor
from ui.layout import Layout
from ui.sidebar import Sidebar


st.set_page_config(
    page_title="Streamlit Supabase Agent OOP",
    page_icon="🧠",
    layout="wide",
)

settings = get_settings()
registry = QueryRegistry()
layout = Layout()
sidebar = Sidebar()
chart_service = ChartService()

if "agent_memory" not in st.session_state:
    st.session_state.agent_memory = SessionMemory()

layout.header()
sidebar.render(registry)

try:
    connection = SupabasePostgresConnection()
    safety_guard = SQLSafetyGuard()
    executor = QueryExecutor(connection, safety_guard)
    router = IntentRouter(registry)
    response_builder = ResponseBuilder()

    agent = StreamlitSupabaseAgent(
        registry=registry,
        router=router,
        executor=executor,
        response_builder=response_builder,
        memory=st.session_state.agent_memory,
    )

    question = layout.question_box()

    col1, col2 = st.columns([1, 3])
    with col1:
        run = st.button("Responder", type="primary", use_container_width=True)

    if run:
        if not question.strip():
            st.warning("Escribe una pregunta primero.")
        else:
            result = agent.answer(question)
            layout.render_result(result, chart_service, show_sql=settings.show_sql)

    with st.expander("Historial de la sesión"):
        st.dataframe(st.session_state.agent_memory.latest(), use_container_width=True)

except Exception as exc:
    st.error("La app no pudo inicializar la conexión o configuración.")
    st.code(str(exc))
    st.info("Revisa tu archivo .env y asegúrate de tener SUPABASE_DATABASE_URL configurado.")
