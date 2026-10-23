import base64
import json
from datetime import date
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import LiveServerTestCase, TestCase, override_settings
from rest_framework.test import APITestCase, APIClient

from .models import Actividad, Proyecto, Tarea


class ApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user('revisor', password='Prueba-local-827!')

    def setUp(self):
        self.client.force_authenticate(self.usuario)
        self.proyecto = Proyecto.objects.create(nombre='Proyecto', fecha_inicio=date(2026, 1, 1))
        self.tarea = Tarea.objects.create(proyecto=self.proyecto, titulo='Tarea')

    def test_crud_completo_en_todas_las_entidades(self):
        casos = [
            ('proyectos', {'nombre': 'Nuevo', 'fecha_inicio': '2026-01-01'}, 'nombre'),
            ('tareas', {'titulo': 'Nueva', 'proyecto': self.proyecto.pk}, 'titulo'),
            ('actividades', {'descripcion': 'Avance', 'tarea': self.tarea.pk}, 'descripcion'),
        ]
        for recurso, datos, campo in casos:
            with self.subTest(recurso=recurso):
                url = f'/api/{recurso}/'
                response = self.client.post(url, datos, format='json')
                self.assertEqual(response.status_code, 201, response.data)
                detalle = f'{url}{response.data["id"]}/'
                self.assertEqual(self.client.get(url).status_code, 200)
                self.assertEqual(self.client.get(detalle).data[campo], datos[campo])
                datos[campo] = 'Reemplazado'
                self.assertEqual(self.client.put(detalle, datos, format='json').status_code, 200)
                response = self.client.patch(detalle, {campo: 'Modificado'}, format='json')
                self.assertEqual(response.status_code, 200, response.data)
                self.assertEqual(self.client.get(detalle).data[campo], 'Modificado')
                self.assertEqual(self.client.delete(detalle).status_code, 204)
                self.assertEqual(self.client.get(detalle).status_code, 404)

    def test_api_requiere_autenticacion_para_todos_los_metodos(self):
        self.client.force_authenticate(None)
        for recurso, pk in [('proyectos', self.proyecto.pk), ('tareas', self.tarea.pk), ('actividades', 1)]:
            for metodo in ['get', 'post', 'put', 'patch', 'delete']:
                with self.subTest(recurso=recurso, metodo=metodo):
                    url = f'/api/{recurso}/' if metodo in ['get', 'post'] else f'/api/{recurso}/{pk}/'
                    self.assertEqual(getattr(self.client, metodo)(url).status_code, 403)

    def test_fechas_invalidas_en_post_y_patch(self):
        datos = {'nombre': 'Fechas', 'fecha_inicio': '2026-02-01', 'fecha_fin': '2026-01-01'}
        self.assertEqual(self.client.post('/api/proyectos/', datos).status_code, 400)
        self.proyecto.fecha_fin = date(2026, 2, 1)
        self.proyecto.save()
        url = f'/api/proyectos/{self.proyecto.pk}/'
        self.assertEqual(self.client.patch(url, {'fecha_inicio': '2026-03-01'}).status_code, 400)
        self.assertEqual(self.client.patch(url, {'fecha_fin': None}, format='json').status_code, 200)

    def test_campos_y_relaciones_invalidas(self):
        for recurso, datos in [
            ('proyectos', {'nombre': ' ', 'fecha_inicio': '2026-01-01'}),
            ('tareas', {'titulo': 'Tarea', 'proyecto': 999999}),
            ('tareas', {'titulo': 'Tarea', 'proyecto': self.proyecto.pk, 'estado': 'invalido'}),
            ('tareas', {'titulo': 'Tarea', 'proyecto': self.proyecto.pk, 'prioridad': 'urgente'}),
            ('actividades', {'descripcion': 'Avance', 'tarea': 999999}),
            ('actividades', {'descripcion': ' ', 'tarea': self.tarea.pk}),
        ]:
            with self.subTest(recurso=recurso, datos=datos):
                self.assertEqual(self.client.post(f'/api/{recurso}/', datos, format='json').status_code, 400)

    def test_borrado_en_cascada(self):
        Actividad.objects.create(tarea=self.tarea, descripcion='Avance')
        self.assertEqual(self.client.delete(f'/api/proyectos/{self.proyecto.pk}/').status_code, 204)
        self.assertFalse(Tarea.objects.exists())
        self.assertFalse(Actividad.objects.exists())

    def test_restricciones_en_base_de_datos(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Proyecto.objects.create(nombre='Invalido', fecha_inicio=date(2026, 2, 1), fecha_fin=date(2026, 1, 1))
        with self.assertRaises(IntegrityError), transaction.atomic():
            Tarea.objects.filter(pk=self.tarea.pk).update(estado='invalido')

    def test_csrf_en_autenticacion_de_sesion(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.usuario)
        response = client.post('/api/proyectos/', {'nombre': 'CSRF', 'fecha_inicio': '2026-01-01'})
        self.assertEqual(response.status_code, 403)


class EvaluacionUnoTests(TestCase):
    def test_pagina_inicial(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inicio.html')
        self.assertContains(response, 'Sistema de Control de Tareas')

    @override_settings(DEBUG=False)
    def test_404_personalizada(self):
        response = self.client.get('/ruta-inexistente/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class ServidorCrudTests(LiveServerTestCase):
    host = '127.0.0.1'

    def test_crud_http_real(self):
        # Servidor local real sobre una base de pruebas aislada.
        get_user_model().objects.create_user('http_revisor', password='Prueba-http-827!')
        token = base64.b64encode(b'http_revisor:Prueba-http-827!').decode()

        # Evita que un proxy del sistema intercepte las peticiones a localhost.
        opener = build_opener(ProxyHandler({}))

        def request(method, path, data=None):
            body = json.dumps(data).encode() if data is not None else None
            req = Request(self.live_server_url + path, data=body, method=method,
                          headers={'Authorization': 'Basic ' + token, 'Content-Type': 'application/json'})
            with opener.open(req, timeout=10) as response:
                raw = response.read()
                return response.status, json.loads(raw) if raw else None

        ids = {}
        casos = [
            ('proyectos', {'nombre': 'HTTP', 'fecha_inicio': '2026-01-01'}, 'nombre'),
            ('tareas', {'titulo': 'HTTP'}, 'titulo'),
            ('actividades', {'descripcion': 'HTTP'}, 'descripcion'),
        ]
        for recurso, datos, campo in casos:
            if recurso == 'tareas':
                datos['proyecto'] = ids['proyectos']
            elif recurso == 'actividades':
                datos['tarea'] = ids['tareas']
            status, obj = request('POST', f'/api/{recurso}/', datos)
            self.assertEqual(status, 201)
            ids[recurso] = obj['id']
            detalle = f'/api/{recurso}/{obj["id"]}/'
            self.assertEqual(request('GET', f'/api/{recurso}/')[0], 200)
            self.assertEqual(request('GET', detalle)[1][campo], 'HTTP')
            datos[campo] = 'PUT HTTP'
            self.assertEqual(request('PUT', detalle, datos)[1][campo], 'PUT HTTP')
            self.assertEqual(request('PATCH', detalle, {campo: 'PATCH HTTP'})[1][campo], 'PATCH HTTP')
        for recurso in reversed(ids):
            detalle = f'/api/{recurso}/{ids[recurso]}/'
            self.assertEqual(request('DELETE', detalle)[0], 204)
            with self.assertRaises(HTTPError) as exc:
                request('GET', detalle)
            self.assertEqual(exc.exception.code, 404)
