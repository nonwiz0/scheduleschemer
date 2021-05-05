from django.urls import path, include
from . import views

app_name = 'ssapp'

urlpatterns = [
    path("", views.Index.as_view(), name='index'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('curriculum', views.Curriculum.as_view(), name='curriculum'),
    path('<str:pk>/profile', views.Profile.as_view(), name='profile'),
    path('signup', views.Signup.as_view(), name='signup'),


    path('login', views.Login.as_view(), name='login'),
]
