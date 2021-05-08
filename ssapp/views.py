from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Class, Account, Curriculum, Course, Program
from django.contrib.auth.models import User
from .forms import SignupForm, ProgramForm, CourseForm
from django.http import Http404, JsonResponse
from picklefield.fields import PickledObjectField
from django.core import serializers

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
        return redirect('ssapp:index')

# Admin site
class AdminProgram(LoginRequiredMixin, generic.CreateView):
    login_url = '/accounts/login'
    form_class = ProgramForm
    template_name = 'ssapp/admin/curriculum.html'

    def get(self, *args, **kwargs):
        all_curr = Program.objects.all()
        form = self.form_class()
        context = {"all_curr": all_curr, "form": form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": ""}, status=400)

class AdminDetailCurriculum(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login'
    model = Program
    template_name = 'ssapp/admin/detail_curriculum.html'


class AdminCourse(LoginRequiredMixin, generic.CreateView):
    template_name = 'ssapp/admin/course.html'
    login_url = '/accounts/login'
    form_class = CourseForm

    def get(self, *args, **kwargs):
        all_courses = Course.objects.all()
        form = self.form_class()
        context = {"all_courses": all_courses, "form": form}
        return render(self.request, self.template_name, context)

class AdminClass(generic.TemplateView):
    template_name = 'ssapp/admin/class.html'
