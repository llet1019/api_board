from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import BoardSerializer
from .models import Board, Category
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

    @action(detail=True, methods=['patch'])
    def update(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs['board_id'])
        try:
            if board.user != request.user:
                result_data = {
                    'code': 502,
                    'data': {},
                    'message': f'글은 작성자만 수정할 수 있습니다.'
                }
            else:
                serializer = BoardSerializer(board, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    result_data = {
                        'code': 200,
                        'data': serializer.data,
                        'message': '수정에 성공하였습니다.'
                    }
                else:
                    result_data = {
                        'code': 500,
                        'data': {},
                        'message': '수정에 실패하였습니다.'
                    }
        except Exception as e:
            result_data = {
                'code': 501,
                'data': {},
                'message': f'{str(e)} 오류가 발생했습니다.'
            }
        return Response(result_data)

    @action(detail=True, methods=['get'])
    def get_info(self, request, *args, **kwargs):
        try:
            board = Board.objects.get(id=kwargs['board_id'])
            serializer = BoardSerializer(board)
            result_data = {
                'code': 200,
                'data': serializer.data,
                'message': '게시물 조회에 성공하였습니다.'
            }
        except Exception as e:
            result_data = {
                'code': 501,
                'data': {},
                'message': f'{str(e)} 오류가 발생했습니다.'
            }
        except Board.DoesNotExist:
            result_data = {
                'code': 404,
                'data': {},
                'message': '존재하지 않는 게시물입니다.'
            }
        return Response(result_data)

    @action(detail=True, methods=['get'])
    def list(self, request, *args, **kwargs):
        try:
            boards = Board.objects.filter(category_id=kwargs['category_id'])
            if boards.count() == 0:
                if Category.objects.filter(id=kwargs['category_id']).exists():
                    result_data = {
                        'code': 200,
                        'data': {},
                        'message': f'게시물이 존재하지 않습니다.'
                    }
                else:
                    result_data = {
                        'code': 404,
                        'data': {},
                        'message': f'존재하지 않는 카테고리입니다.'
                    }
            else:
                serializer = BoardSerializer(boards, many=True)
                result_data = {
                    'code': 200,
                    'data': serializer.data,
                    'message': f'게시판 조회에 성공하였습니다.'
                }
        except Exception as e:
            result_data = {
                'code': 501,
                'data': {},
                'message': f'{str(e)} 오류가 발생했습니다.'
            }
        return Response(result_data)
