from django.shortcuts import render


def inicio(request):
    nombre_proyecto = "Sistema de Control de Tareas"

    funcionalidades = [
        "Gestión de proyectos",
        "Control de tareas",
        "Seguimiento de actividades",
    ]

    cantidad_funcionalidades = len(funcionalidades)

    if cantidad_funcionalidades > 0:
        estado = "Sistema inicial configurado"
    else:
        estado = "Sin funcionalidades definidas"

    datos = {
        "nombre_proyecto": nombre_proyecto,
        "descripcion": "Plataforma orientada a centralizar la gestión de proyectos, tareas y seguimiento de actividades.",
        "funcionalidades": funcionalidades,
        "cantidad_funcionalidades": cantidad_funcionalidades,
        "estado": estado,
    }

    return render(request, "inicio.html", datos)


def error_404(request, exception):
    return render(request, "404.html", status=404)