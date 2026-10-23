-- Ejecutar como administrador DESPUES de crear control_tareas_app.
GRANT ALL PRIVILEGES ON control_tareas.* TO 'control_tareas_app'@'localhost';
-- Permisos limitados a esta base; sin privilegios globales ni GRANT OPTION.
-- GRANT/CREATE USER se aplican inmediatamente: no se requiere FLUSH PRIVILEGES.
