from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sistema_control.urls')),
]


handler404 = 'sistema_control.views.error_404'