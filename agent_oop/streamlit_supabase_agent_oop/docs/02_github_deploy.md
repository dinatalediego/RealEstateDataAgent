# Guía GitHub + despliegue web

## 1. Crear repo

```bash
git init
git add .
git commit -m "initial streamlit supabase agent oop"
git branch -M main
git remote add origin https://github.com/USUARIO/streamlit-supabase-agent-oop.git
git push -u origin main
```

## 2. Revisar seguridad antes del push

```bash
git status
```

Confirmar que `.env` no aparece.

## 3. Deploy recomendado

Opciones:

- Streamlit Community Cloud: simple para demo.
- Render: bueno para app privada simple.
- Railway: rápido para prototipos.
- VPS o Docker: más control.

## 4. Secrets

En la plataforma de despliegue agregar:

```env
SUPABASE_DATABASE_URL=postgresql+psycopg2://...
APP_ENV=production
MAX_ROWS=500
SHOW_SQL=false
```

En producción puedes ocultar SQL con `SHOW_SQL=false`.

## 5. Checklist antes de compartir

- Usuario de BD read-only.
- RLS configurado si aplica.
- Sin claves en GitHub.
- Consultas limitadas.
- Logs habilitados.
- Mensajes de error entendibles.
