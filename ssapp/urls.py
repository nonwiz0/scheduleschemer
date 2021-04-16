from django.urls import path, include
from . import views

app_name = 'ssapp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.Login.as_view(), name='login'),
]
