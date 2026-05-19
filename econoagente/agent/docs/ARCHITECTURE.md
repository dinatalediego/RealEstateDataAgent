# Arquitectura DecideCasa AgentOS

## Principio central

El agente no debe ser una clase gigante. Debe ser una organización de objetos pequeños.

```text
Usuario
  ↓
AgentWorkspace / Streamlit UI
  ↓
AgentCouncil
  ↓
RealEstateDataAgent
  ↓
BusinessQuestionRouter
  ↓
BusinessQuestionCatalog
  ↓
QueryShield
  ↓
SupabaseQueryRunner
  ↓
DataTrustMeter
  ↓
ExecutiveInsightBuilder
  ↓
Respuesta + Tabla + Gráfico + SQL + Confianza
```

## Clases clave

| Clase | Problema menor que resuelve |
|---|---|
| `AgentCouncil` | Coordinar agentes |
| `RealEstateDataAgent` | Orquestar la respuesta |
| `BusinessQuestionRouter` | Detectar intención |
| `BusinessQuestionCatalog` | Guardar SQL aprobado |
| `QueryShield` | Evitar SQL peligroso |
| `SupabaseQueryRunner` | Ejecutar consulta |
| `DataTrustMeter` | Medir confianza |
| `ExecutiveInsightBuilder` | Convertir datos en insight |
| `InsightChartBuilder` | Crear visual |
| `QueryAuditTrail` | Registrar trazabilidad |

## Por qué no SQL libre desde el inicio

Porque un agente que genera SQL libre puede:

- consultar tablas incorrectas,
- inventar columnas,
- consumir demasiado,
- exponer datos sensibles,
- ejecutar operaciones peligrosas si está mal protegido.

Por eso esta versión usa un catálogo seguro.
