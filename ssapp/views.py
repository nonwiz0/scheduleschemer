from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Class

# Create your views here.
class Index(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login'
    template_name = 'ssapp/index.html' 
    model = Class

class Login(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/login.html'