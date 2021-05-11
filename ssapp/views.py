from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Class, Account, Curriculum, Course, ClassSchedule
from django.contrib.auth.models import User
from .forms import SignupForm, CurriculumForm, CourseForm, EnrollCourseForm
from django.http import Http404, JsonResponse
from picklefield.fields import PickledObjectField
from django.core import serializers
import json
# Create your views here.
class Index(generic.ListView):
    template_name = 'ssapp/index.html'
    model = Account

class Dashboard(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/dashboard.html' 
 
    def get(self, *args, **kwargs):
        account = Account.objects.filter(user=self.request.user)[0]
        courses = account.enrolled_class.all()
        context = {"account": account, "class_list": courses}
        return render(self.request, self.template_name, context)


class DetailProfile(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/profile.html'
    
    def get(self, *args, **kwargs):
        account = Account.objects.filter(user=self.request.user)[0]
        courses = account.enrolled_class.all()
        context = {"account": account, "courses": courses}
        return render(self.request, self.template_name, context)

class UserCurriculum(LoginRequiredMixin, generic.TemplateView):
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
        major = Curriculum.objects.filter(name=self.request.POST['major'])[0]
        new_acc = Account(user=new_user, major=major)
        new_acc.save()
        return redirect('ssapp:dashboard')

class ManageCourse(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/course.html'


class UserEnrollCourse(LoginRequiredMixin, generic.UpdateView):
    login_url = '/accounts/login'
    form_class = EnrollCourseForm
    template_name = 'ssapp/course.html'

    def get(self, *args, **kwargs):
        form = self.form_class()
        account = Account.objects.get(user=self.request.user)
        courses = account.enrolled_class.all()
        total = 0
        for one_class in courses:
            total += one_class.course.credits
        context = {"form": form, 'courses': courses, 'total': total}
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


# Admin site
class AdminCurriculum(LoginRequiredMixin, generic.CreateView):
    login_url = '/accounts/login'
    form_class = CurriculumForm
    template_name = 'ssapp/admin/curriculum.html'

    def get(self, *args, **kwargs):
        all_curr = Curriculum.objects.all()
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
    model = Curriculum
    template_name = 'ssapp/admin/detail_curriculum.html'


class AdminCourse(LoginRequiredMixin, generic.CreateView):
    template_name = 'ssapp/admin/course.html'
    login_url = '/accounts/login'
    form_class = CourseForm

    def get(self, *args, **kwargs):
        form = self.form_class()
        context = {"all_courses": Course.objects.all(), "form": form}
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

class AdminDetailCourse(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login'
    model = Course
    template_name = 'ssapp/admin/class.html'

    def get(self, *args, **kwargs):
        course_id = Course.objects.filter(pk=self.kwargs['pk'])[0]
        print(course_id) 
        schedule = ClassSchedule.objects.filter(course=course_id)
        new_schedule = dict()
        if len(schedule):
            for x in schedule:
                for y in x.daytime: 
                    new_schedule[y] = x.daytime[y]
            schedule = new_schedule
        else:
            schedule = dict() 
        context = {"schedule": schedule, "course": course_id}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        course_id = Course.objects.get(pk=self.kwargs['pk'])
        daytime = json.loads(self.request.POST.get('daytime', ''))
        daytime = daytime["daytime"]
        session = dict()
        for key, val in daytime.items():
            if key in ["Mon", "Tue" , "Wed", "Thu", "Fri"]:
                session[key] = [val[0], val[1]]
        if ClassSchedule.objects.filter(course=course_id).exists():
            print(True)
            prev_class = ClassSchedule.objects.get(course=course_id)
            for day in daytime:
                prev_class.daytime[day] = session[day]
            prev_class.save()
        else:
            curr_class = ClassSchedule(course=course_id, availability=True, daytime=session)
            curr_class.save()
            curr_class = Class(id=course_id.id, availability=True, daytime=session)
            curr_class.save()
            print("daytime", session)
        return JsonResponse({"instance": ""}, status=200)




class AdminClass(generic.TemplateView):
    template_name = 'ssapp/admin/class.html'


def UpdateSchedule(request):
    print(request.POST)
