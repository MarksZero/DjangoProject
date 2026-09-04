# Sistema de Control de Tareas

Proyecto orientado a centralizar la gestión de proyectos, tareas y el seguimiento de actividades dentro de una organización.

Esta primera etapa implementa la estructura inicial de Django, la aplicación `sistema_control`, rutas propias, una página de bienvenida y una página de error 404 personalizada.

## Tecnologías

- Python 3.13
- Django 6.1

## Instalación en Windows

Abre una terminal de PowerShell y sigue estos pasos:

1. Clona el repositorio.

   ```powershell
   git clone  https://github.com/MarksZero/DjangoProject
   ```

2. Entra a la carpeta del proyecto:

   ```powershell
   cd DjangoProject
   ```

3. Crea el ambiente virtual:

   ```powershell
   py -m venv .venv
   ```

4. Activa el ambiente virtual:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Instala las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```
   
## Variable de entorno requerida

Antes de ejecutar el proyecto debe configurarse `DJANGO_SECRET_KEY`.

En PowerShell para generar una nueva clave:
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Luego con la nueva clave generada en la terminal:
```powershell
$env:DJANGO_SECRET_KEY = "la_nueva_clave"
```
```Linux
set -x DJANGO_SECRET_KEY 'tu_clave'
```

### Aplicar migraciones iniciales de Django

En una instalación nueva, ejecutar:

```bash
python manage.py migrate

## Ejecución

Desde la carpeta que contiene `manage.py`, con el ambiente virtual activo, ejecuta:

```powershell
python manage.py runserver
```

Abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en el navegador.

## Funcionalidades implementadas

- Estructura inicial del proyecto Django configurada.
- Aplicación `sistema_control` registrada.
- Rutas propias de la aplicación.
- Página de bienvenida.
- Página de error 404 personalizada.
- Dependencias registradas en `requirements.txt`.

