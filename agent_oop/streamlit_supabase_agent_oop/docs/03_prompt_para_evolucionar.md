# Prompt para evolucionar este proyecto en otra consulta

Quiero evolucionar este proyecto `streamlit_supabase_agent_oop`.

Contexto:

- Tengo una app Streamlit conectada a Supabase/Postgres.
- La arquitectura es OOP y modular.
- `app.py` solo debe orquestar.
- `core/` contiene el agente, router de intención, respuesta, memoria y seguridad.
- `database/` contiene conexión, diccionario de datos y catálogo de SQL autorizado.
- `services/` contiene ejecución SQL y gráficos.
- `ui/` contiene layout y componentes visuales.

Objetivo:

Convertirlo en un agente web inmobiliario capaz de responder preguntas clave sobre inventario, ventas, cobranzas, clientes, calidad de datos y geografía.

Restricciones importantes:

1. No ejecutar SQL libre sin validación.
2. Usar usuario read-only.
3. Mantener catálogo de preguntas autorizadas.
4. Mostrar tabla, gráfico e insight.
5. Registrar historial de preguntas.
6. Preparar para GitHub y despliegue.
7. No subir `.env`.

Quiero que generes mejoras en:

- Catálogo de preguntas.
- Diccionario de datos.
- UI ejecutiva.
- Manejo de errores.
- Seguridad SQL.
- Roles de agentes.
- Deploy.
- README.

Además, adapta los SQL a mis tablas reales de Supabase si te comparto sus nombres y columnas.
