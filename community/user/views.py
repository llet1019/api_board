from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth import authenticate
from django.conf import settings

from .serializer import UserSerializer, UserDataSerializer, TokenObtainPairSerializer
import jwt

from .models import User


class UserRegisterViewSets(viewsets.ModelViewSet):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.FORMAT_PASSWORD)
            },
        ), )
    @action(detail=True, methods=['post'])
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            result_data = Response(
                {
                    'user': serializer.data,
                    'message': 'register successs',
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            result_data.set_cookie('access', access_token, httponly=True)
            result_data.set_cookie('refresh', refresh_token, httponly=True)
            return result_data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSets(viewsets.ModelViewSet):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.FORMAT_PASSWORD)
            },
        ),)
    @action(detail=True, methods=['post'])
    def login(self, request, *args, **kwargs):
        user = authenticate(
            email=request.data.get('email'), password=request.data.get('password')
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            result_data = Response(
                {
                    'user': serializer.data,
                    'message': 'login success',
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            result_data.set_cookie('access', access_token, httponly=True)
            result_data.set_cookie('refresh', refresh_token, httponly=True)
            return result_data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def logout(self, request, *args, **kwargs):
        try:
            result_data = Response({
                'message': 'Logout success'
            }, status=status.HTTP_202_ACCEPTED)
            result_data.delete_cookie('access')
            result_data.delete_cookie('refresh')
        except Exception as e:
            print(e)
            result_data = Response({
                'message': f'{str(e)} error occurred'
            })
        return result_data


class UserViewSets(viewsets.ModelViewSet):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description='Bearer',
                                             type=openapi.TYPE_STRING)]
    )
    @action(detail=True, methods=['get'])
    def get_info(self, request, *args, **kwargs):
        authorization_header = request.headers.get('Authorization')

        access_token = authorization_header.split(' ')[1]
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256']
        )
        if payload != kwargs['user_id']:
            result_data = {
                'code': 400,
                'data': {},
                'message': '올바르지 않은 토큰입니다.'
            }
            return Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=payload['user_id'])
        try:
            serializer = UserDataSerializer(user)
            result_data = {
                'code': 200,
                'data': serializer.data
            }
            res_status = 200
        except Exception as e:
            print(e)
            result_data = {
                'code': 400,
                'data': {}
            }
            res_status = 400
        return Response(result_data, status=res_status)