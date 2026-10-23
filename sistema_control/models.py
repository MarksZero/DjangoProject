from django.db import models
from django.db.models import F, Q


class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        constraints = [models.CheckConstraint(
            condition=Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=F('fecha_inicio')),
            name='proyecto_fechas_validas',
        )]

    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        EN_PROGRESO = 'en_progreso', 'En progreso'
        COMPLETADA = 'completada', 'Completada'

    class Prioridad(models.TextChoices):
        BAJA = 'baja', 'Baja'
        MEDIA = 'media', 'Media'
        ALTA = 'alta', 'Alta'

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    prioridad = models.CharField(max_length=10, choices=Prioridad.choices, default=Prioridad.MEDIA)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        constraints = [
            models.CheckConstraint(condition=Q(estado__in=['pendiente', 'en_progreso', 'completada']), name='tarea_estado_valido'),
            models.CheckConstraint(condition=Q(prioridad__in=['baja', 'media', 'alta']), name='tarea_prioridad_valida'),
        ]

    def __str__(self):
        return self.titulo


class Actividad(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='actividades')
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'actividades'

    def __str__(self):
        return self.descripcion[:80]
