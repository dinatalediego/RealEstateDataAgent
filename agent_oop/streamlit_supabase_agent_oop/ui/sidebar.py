import streamlit as st
from database.query_registry import QueryRegistry


class Sidebar:
    def render(self, registry: QueryRegistry):
        st.sidebar.title("🧠 Agent Control")
        st.sidebar.caption("Preguntas autorizadas disponibles")

        area_filter = st.sidebar.selectbox(
            "Área",
            ["Todas"] + sorted({q.area for q in registry.all()})
        )

        st.sidebar.divider()
        for q in registry.all():
            if area_filter != "Todas" and q.area != area_filter:
                continue
            st.sidebar.markdown(f"**{q.title}**")
            st.sidebar.caption(q.area)

        return area_filter
