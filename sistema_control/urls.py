from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('proyectos', views.ProyectoViewSet)
router.register('tareas', views.TareaViewSet)
router.register('actividades', views.ActividadViewSet)

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
