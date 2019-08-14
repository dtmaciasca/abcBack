from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.serializers import *
from .serializers import EventoSerializer, CategoriaSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import *
import json, datetime
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
# Create your views here.

@csrf_exempt
def postEvento(request):
    if request.method == 'POST':
        try:
            json_evento = json.loads(request.body)
            user = User.objects.get(id=json_evento['user'])
            categoria = Categoria.objects.get(id=json_evento['categoria'])
            evento_model = Evento(
            nombre = json_evento['nombre'],
            categoria=categoria,
            lugar=json_evento['lugar'],
            direccion=json_evento['direccion'],
            fecha_inicio=datetime.datetime.strptime(json_evento['fecha_inicio'], '%Y-%m-%d'),
            fecha_fin=datetime.datetime.strptime(json_evento['fecha_fin'], '%Y-%m-%d'),
            es_presencial=json_evento['es_presencial'],
            user=user)
            evento_model.save()

            return HttpResponse(serialize("json", [evento_model]))
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )

@csrf_exempt
def getAllCategorias(request):
    try:
        data = Categoria.objects.all()
        if request.method == 'GET':
            serializer = CategoriaSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST
        )

@csrf_exempt
def putEvento(request, idEvento):
    if request.method == 'PUT':
        evento = Evento.objects.get(id=idEvento);
        try:
            json_evento = json.loads(request.body)
            if (json_evento['categoria'] != None):
                categoria = Categoria.objects.get(id=json_evento['categoria'])
                evento.categoria = categoria

            if (json_evento['nombre'] != None):
                evento.nombre = json_evento['nombre']

            if (json_evento['lugar'] != None):
                evento.lugar=json_evento['lugar']

            if (json_evento['direccion'] != None):
                evento.direccion=json_evento['direccion']

            if (json_evento['fecha_inicio'] != None):
                evento.fecha_inicio=json_evento['fecha_inicio']

            if (json_evento['fecha_fin'] != None):
                evento.fecha_fin=json_evento['fecha_fin']

            if (json_evento['es_presencial'] != None):
                evento.es_presencial=json_evento['es_presencial']
            evento.save()

            return HttpResponse(status=HTTP_200_OK)
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )

@csrf_exempt
def getAllEventos(request, idUser):
    try:
        eventos = Evento.objects.filter(user=idUser).order_by('-fecha_creacion')
        if request.method == 'GET':
            serializer = EventoSerializer(eventos, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST
        )

@csrf_exempt
def deleteEvento(request, idEvento):
    if request.method == 'DELETE':
        try:
            a="ok"
            evento = Evento.objects.get(id=idEvento)
            print('llego ahi')
            evento.delete()
            return HttpResponse(status=HTTP_200_OK)
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )

def getDetailEvento(request, idEvento):
    data = Evento.objects.filter(id=idEvento)
    print(data)
    if request.method == 'GET':
        serializer = EventoSerializer(data, many=True)
        print(serializer.data)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is "" or password is "":
        return Response({'error': 'Debe ingresar usuario y contraseña'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user == None:
        return Response({'error': 'Credenciales inválidas'}, status=HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username,
                     'firstName': user.first_name, 'lastName': user.last_name, 'id': user.id}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getTokenVal(request):
    if request.method == 'GET':
        token = request.META['HTTP_AUTHORIZATION']
        token = token.replace('Token ', '')
        try:
            TokenStatus = Token.objects.get(key=token).user.is_active
        except Token.DoesNotExist:
            TokenStatus = False
        if TokenStatus == True:
            return Response({'mensaje': 'Token valido'}, status=HTTP_200_OK)
        else:
            return Response({'error': 'Token inválido'}, status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def logout(request):
    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    try:
        TokenStatus = Token.objects.get(key=token).user.is_active
    except Token.DoesNotExist:
        TokenStatus = False
    if TokenStatus == True:
        Token.objects.filter(key=token).delete()
        return Response({'mensaje': 'Sesión finalizada'}, status=HTTP_200_OK)
    else:
        return Response({'error': 'Token no existe'}, status=HTTP_404_NOT_FOUND)

@csrf_exempt
def postUser(request):
    if request.method == 'POST':
        print(request.body)
        user_model = None
        try:
            json_user = json.loads(request.body)
            username = json_user['username']
            password = json_user['password']
            first_name = json_user['first_name']
            last_name = json_user['last_name']
            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = username
            user_model.save()

            return HttpResponse(serialize("json", [user_model]))
        except KeyError as e:
            return HttpResponseBadRequest(
                content='El campo ' + str(e) + ' es requerido.'
            )
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                return HttpResponseBadRequest(
                    content='Ya existe un usuario con ese correo. '
                )
        except Exception as ex:
            print(ex)
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )
