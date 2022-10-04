from django.urls import path

from . import views

urlpatterns = [
    path('user/signup/',
         views.UserRegisterViewSets.as_view({'post': 'create'})),
    path('user/login/',
         views.UserLoginViewSets.as_view({'post': 'login'})),
    path('user/logout/',
         views.UserLoginViewSets.as_view({'delete': 'logout'})),
    path('user/<int:user_id>/',
         views.UserViewSets.as_view({'get': 'get_info'})),
]