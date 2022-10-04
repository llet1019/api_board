from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import BoardSerializer
from .models import Board
from user.models import User


class BoardViewSets(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            result_data = {
                'code': 500,
                'data': {},
                'message': '로그인한 유저만 작성 가능합니다.'
            }
            return Response(result_data, status=500)
        else:
            serializer = BoardSerializer(data=request.data)
            try:
                if serializer.is_valid():
                    serializer.save()
                    result_data = {
                        'code': 200,
                        'data': serializer.data,
                        'message': '게시물 작성에 성공하였습니다.'
                    }
                    return Response(result_data, status=200)
            except Exception as e:
                result_data = {
                    'code': 400,
                    'data': {},
                    'message': f'{str(e)} 오류가 발생하였습니다.'
                }
                return Response(result_data, status=400)
