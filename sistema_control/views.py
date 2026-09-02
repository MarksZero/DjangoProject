from django.shortcuts import render


def inicio(request):
    contexto = {
        "nombre_proyecto": "Sistema de Control de Tareas",
        "descripcion": "Plataforma orientada a centralizar la gestión de proyectos, tareas y seguimiento de actividades.",
    }

    return render(request, "inicio.html", contexto)

def error_404(request, exception):
    return render(request, "404.html", status=404)