from django.urls import path

from . import views

urlpatterns = [
    path('board/',
         views.BoardViewSets.as_view({'post': 'create'})),
    path('board/<int:board_id>/',
         views.BoardViewSets.as_view(
             {'get': 'get_info', 'patch': 'update', 'delete': 'destroy'}
         )),
    path('category/<int:category_id>/board/',
         views.BoardViewSets.as_view({'get': 'list'})),
]