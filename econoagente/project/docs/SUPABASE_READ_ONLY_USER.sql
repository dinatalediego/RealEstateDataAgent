-- Opcional / avanzado: crear usuario read-only en Postgres/Supabase.
-- Ejecutar con un usuario administrador. Ajusta password y schemas.

-- create role agent_readonly login password 'CAMBIAR_PASSWORD_SEGURO';
-- grant usage on schema gold to agent_readonly;
-- grant usage on schema mart to agent_readonly;
-- grant select on all tables in schema gold to agent_readonly;
-- grant select on all tables in schema mart to agent_readonly;
-- alter default privileges in schema gold grant select on tables to agent_readonly;
-- alter default privileges in schema mart grant select on tables to agent_readonly;

-- Validación:
-- set role agent_readonly;
-- select * from gold.dim_project limit 5;
