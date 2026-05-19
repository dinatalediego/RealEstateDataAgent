import streamlit as st


class Layout:
    def header(self):
        st.title("🧠 Streamlit Supabase Agent OOP")
        st.caption(
            "Agente web para responder preguntas clave sobre Supabase con SQL autorizado, "
            "OOP, trazabilidad y visualización ejecutiva."
        )

    def question_box(self) -> str:
        examples = [
            "¿Cuántas unidades disponibles hay por proyecto?",
            "¿Cuál es el precio promedio por m2 por distrito?",
            "¿Cuánto se ha cobrado por proyecto?",
            "¿Qué asesor tiene más ventas?",
            "¿Qué problemas de calidad de datos existen?",
            "¿Qué distritos concentran más compradores?",
        ]

        selected = st.selectbox("Ejemplos de preguntas", [""] + examples)
        typed = st.text_input("Pregunta", value=selected, placeholder="Escribe una pregunta del negocio...")
        return typed

    def render_result(self, result, chart_service, show_sql: bool = True):
        st.subheader("Respuesta")
        st.write(result.answer)

        if result.error:
            st.error(result.error)

        if result.data is not None:
            fig = chart_service.build_chart(result.data, result.chart_type or "bar")
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(result.data, use_container_width=True)

        if show_sql and result.sql:
            with st.expander("Ver SQL utilizado"):
                st.code(result.sql, language="sql")
