# 🚀 Guía paso a paso para desplegar DecideCasa AgentOS

## Opción A — Streamlit Community Cloud

### Paso 1: Crear repo en GitHub

```bash
git init
git add .
git commit -m "Initial DecideCasa AgentOS"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/decidecasa-agentos.git
git push -u origin main
```

### Paso 2: Verificar archivos importantes

Deben estar en GitHub:

```text
app.py
requirements.txt
README.md
config/query_catalog.yaml
src/decidecasa_agentos/
.env.example
```

No debe estar:

```text
.env
.streamlit/secrets.toml
```

### Paso 3: Crear app en Streamlit Cloud

1. Entrar a Streamlit Community Cloud.
2. New app.
3. Seleccionar repo.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Deploy.

### Paso 4: Agregar secrets

En App > Settings > Secrets, pegar:

```toml
APP_MODE = "production"
SUPABASE_DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require"
AGENT_ALLOWED_SCHEMAS = "gold,mart,public"
AGENT_MAX_ROWS = "500"
AGENT_QUERY_TIMEOUT_SECONDS = "20"
AGENT_LOG_PATH = "logs/query_audit.csv"
```

Streamlit expone estos secrets como variables de entorno para la app.

### Paso 5: Probar conexión

Al abrir la app, revisar el sidebar:

```text
Conexión Supabase/Postgres OK.
```

Si falla:

- Revisar usuario/password.
- Revisar puerto.
- Revisar `sslmode=require`.
- Revisar que Supabase acepte conexión desde internet.
- Revisar que el usuario tenga permisos SELECT.

---

## Opción B — Render

### Paso 1: Subir a GitHub

Igual que arriba.

### Paso 2: Crear Web Service en Render

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### Paso 3: Environment variables

Agregar:

```text
APP_MODE=production
SUPABASE_DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require
AGENT_ALLOWED_SCHEMAS=gold,mart,public
AGENT_MAX_ROWS=500
AGENT_QUERY_TIMEOUT_SECONDS=20
```

---

## Opción C — Railway

Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Variables iguales a Render.

---

# Checklist PRO antes de producción

## Seguridad

- Crear usuario read-only en Supabase/Postgres.
- No usar `service_role_key`.
- No subir `.env`.
- Mantener `QueryShield` activo.
- Usar solo schemas `gold`, `mart` y/o `public` según necesidad.

## Datos

- Validar que las tablas del catálogo existan.
- Probar cada SQL en Supabase SQL Editor.
- Confirmar nombres de columnas.
- Confirmar tipos numéricos y fechas.

## Producto

- Agregar preguntas sugeridas reales.
- Agregar filtros por proyecto/fuente/distrito.
- Agregar login si el uso será interno.
- Agregar auditoría persistente en Supabase si será multiusuario.

## Evolución

- V1: Catálogo seguro de preguntas.
- V2: Filtros dinámicos.
- V3: Agentes por dominio: Comercial, Inventario, Finanzas, Calidad, Geo.
- V4: Generación SQL asistida, pero validada por catálogo/políticas.
- V5: Control de usuarios, roles y auditoría centralizada.
