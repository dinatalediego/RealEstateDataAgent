# Qué era lo más importante que no se estaba considerando

## 1. Seguridad antes que inteligencia

El mayor riesgo es dejar que un agente genere SQL libre y lo ejecute directamente contra Supabase.

La primera versión debe usar:

- Usuario read-only.
- Catálogo de consultas autorizadas.
- Bloqueo de `insert`, `update`, `delete`, `drop`, `alter`, etc.
- Límite de filas.
- Logs de preguntas y consultas ejecutadas.

## 2. Diccionario de datos

El agente necesita saber qué significa cada tabla, no solo su nombre técnico.

Ejemplo:

```text
gold.fact_cobranzas = ventas, montos cobrados, pendientes y avance financiero.
gold.fact_inventory = unidades, proyectos, estados comerciales y precio m2.
```

Sin diccionario de datos, el agente puede responder con tablas incorrectas.

## 3. Separar interfaz de lógica

Streamlit no debe contener todo.

Correcto:

```text
app.py = orquestador
core/ = cerebro del agente
database/ = conexión y SQL autorizado
services/ = ejecución y gráficos
ui/ = componentes visuales
```

## 4. Trazabilidad

Toda respuesta importante debería poder contestar:

- ¿Qué pregunta hizo el usuario?
- ¿Qué intención detectó el agente?
- ¿Qué SQL ejecutó?
- ¿Cuántas filas devolvió?
- ¿Hubo error?

## 5. Versionamiento en GitHub

GitHub no es solo almacenamiento. Es la memoria compartida de los agentes.

Debe incluir:

- README.
- `.env.example`.
- `.gitignore`.
- requirements.
- estructura modular.
- ejemplos de preguntas.
- documentación de despliegue.

## 6. Roles de agentes

La evolución correcta no es un único agente gigante.

Debe evolucionar a:

- Agent Comercial.
- Agent Inventario.
- Agent Finanzas.
- Agent Calidad de datos.
- Agent Geo.
- Agent Ejecutivo.

## 7. Permisos por usuario

No todos deberían ver todo.

Ejemplo:

- Comercial ve ventas, leads y asesores.
- Finanzas ve cobranzas.
- Gerencia ve consolidado.
- Calidad ve inconsistencias.

## 8. Respuesta ejecutiva

No basta devolver una tabla.

Una buena respuesta debe traer:

- Insight corto.
- Tabla.
- Gráfico.
- SQL utilizado.
- Acción sugerida.

## 9. No depender de una sola tabla

Muchas preguntas reales requerirán cruces entre:

- Proyectos.
- Unidades.
- Ventas.
- Cobranzas.
- Clientes.
- Ubicaciones.
- Calidad de datos.

Por eso conviene tener capa `gold` o vistas mart listas para consumo.

## 10. Preparar la app para fallar bien

Una app profesional no solo funciona cuando todo está perfecto.

Debe explicar:

- Falta conexión.
- Falta tabla.
- Falta columna.
- Pregunta no autorizada.
- Consulta sin resultados.
