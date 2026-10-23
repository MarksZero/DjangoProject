from rest_framework import serializers
from .models import Actividad, Proyecto, Tarea


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']

    def validate(self, attrs):
        inicio = attrs.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        fin = attrs.get('fecha_fin', getattr(self.instance, 'fecha_fin', None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({'fecha_fin': 'No puede ser anterior a fecha_inicio.'})
        return attrs


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'proyecto', 'titulo', 'descripcion', 'estado', 'prioridad', 'fecha_creacion', 'fecha_limite']
        read_only_fields = ['fecha_creacion']


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'tarea', 'descripcion', 'fecha']
        read_only_fields = ['fecha']
