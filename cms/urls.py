
from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register',views.userRegister),
    path('login',views.userLogin),
    path('contentItem',views.contentItem),
    path('contentItem/<int:pk>',views.contentItemDetail),
]