from django.contrib import admin
from .models import Actividad, Proyecto, Tarea


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre']


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'proyecto', 'estado', 'prioridad']
    list_filter = ['estado', 'prioridad']
    search_fields = ['titulo']
    list_select_related = ['proyecto']


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['id', 'tarea', 'fecha']
    list_select_related = ['tarea']
