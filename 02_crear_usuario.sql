-- MySQL 8.0.18+ genera una contrasena aleatoria: guardar el resultado en DB_PASSWORD.
-- Ejecutar antes de 02_permisos.sql. No guarda credenciales en el archivo.
CREATE USER 'control_tareas_app'@'localhost' IDENTIFIED BY RANDOM PASSWORD;
