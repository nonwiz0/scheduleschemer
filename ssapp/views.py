from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Class, Account
from django.contrib.auth.models import User
from .forms import SignupForm
from django.http import Http404

# Create your views here.
class Index(generic.ListView):
    template_name = 'ssapp/index.html'
    model = Account

class Dashboard(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login'
    template_name = 'ssapp/dashboard.html' 
    model = Class

class Profile(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/profile.html'

class Curriculum(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/curriculum.html'
 
class Login(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/login.html'

class Signup(generic.CreateView):
    model = Account
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        username = form.cleaned_data['username']
        new_user = User.objects.create_user(username=username, password=form.cleaned_data['password1'], email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
        new_user.save()
        new_acc = Account(user=new_user, major=self.request.POST['major'], faculty=self.request.POST['faculty'], enrolled_course={})
        new_acc.save()
        return redirect('ssapp:dashboard')

