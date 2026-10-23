# Sistema de Control de Tareas

Proyecto Django con API REST para gestionar proyectos, tareas y actividades.

## Requisitos

Git y Python 3.13. SQLite permite ejecutar el proyecto sin instalar un servidor de base de datos.
Ejecutar los comandos desde la carpeta que contiene `manage.py`.

## Instalación

### Windows · PowerShell

```powershell
cd C:\Users\pablo\PycharmProjects\DjangoProject
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación, usar `.\.venv\Scripts\python.exe` en lugar de `python`.

### CachyOS · Bash

```bash
sudo pacman -Syu --needed python python-pip git base-devel pkgconf mariadb-libs
cd DjangoProject
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Entrar a la ubicación real del proyecto antes de crear el entorno. Si la terminal usa Fish, ejecutar `bash`.
Crear `.venv` en cada equipo; no copiarlo entre Windows y Linux.

## Configuración

El proyecto utiliza un archivo `.env` junto a `manage.py` para desacoplar la configuración sensible de `settings.py`.

La estructura de configuración utilizada es:

```dotenv
DJANGO_SECRET_KEY='CLAVE_DEL_PROYECTO'
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=sqlite
```

Para esta evaluación, el archivo `.env` forma parte de la entrega y se encuentra incluido en el repositorio según las instrucciones proporcionadas.

No subir `.venv` ni `db.sqlite3` a Git.

## Levantar la web

Con el entorno activo, ejecutar la primera vez:

```text
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000 --insecure
```

`createsuperuser` crea las credenciales del administrador y de la API.
`--insecure` permite cargar sus estilos con `DEBUG=false`; usarlo solo para desarrollo local.

- Web: http://127.0.0.1:8000/
- Administración: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/
- Iniciar sesión: http://127.0.0.1:8000/api-auth/login/?next=/api/

La API requiere autenticación. Detener el servidor con Ctrl+C.

Para volver a ejecutar, entrar a la carpeta del proyecto y activar el entorno:

```powershell
# Windows
.\.venv\Scripts\Activate.ps1
```

```bash
# CachyOS con Bash
source .venv/bin/activate
```

Después, en ambos sistemas:

```text
python manage.py runserver 127.0.0.1:8000 --insecure
```

No es necesario recrear el entorno ni el usuario. Ejecutar `migrate` cuando haya migraciones nuevas.

## Configuración MySQL

El proyecto incluye los scripts SQL solicitados para crear la base de datos, el usuario de aplicación y sus permisos.

Con MySQL 8.4 instalado y activo, ejecutar una sola vez desde la raíz del proyecto:

```text
mysql -u root -p -e "source sql/01_crear_base.sql"
mysql -u root -p -e "source sql/02_crear_usuario.sql"
mysql -u root -p -e "source sql/03_permisos.sql"
```

El segundo script devuelve la contraseña del usuario creado. Para utilizar MySQL, reemplazar `DB_ENGINE=sqlite` en `.env` y añadir los datos de conexión:

```dotenv
DB_ENGINE=mysql
DB_NAME=control_tareas
DB_USER=control_tareas_app
DB_PASSWORD='PEGAR_LA_CONTRASEÑA_DEL_USUARIO_SQL'
DB_HOST=localhost
DB_PORT=3306
```

Ejecutar `migrate` y `createsuperuser` en esa base. Cambiar de motor no copia los datos de SQLite.
El script `02_crear_usuario.sql` es específico de MySQL y no se ejecuta directamente en MariaDB.

## API

| Recurso | Listar y crear | Consultar, editar y eliminar |
|---|---|---|
| Proyectos | `/api/proyectos/` | `/api/proyectos/{id}/` |
| Tareas | `/api/tareas/` | `/api/tareas/{id}/` |
| Actividades | `/api/actividades/` | `/api/actividades/{id}/` |

Las colecciones admiten GET/POST; el detalle, GET/PUT/PATCH/DELETE.
Eliminar un proyecto elimina sus tareas y actividades. Los usuarios autenticados comparten el acceso a los registros.

## Pruebas

```text
python manage.py check
python manage.py test sistema_control
python -m pip check
```
