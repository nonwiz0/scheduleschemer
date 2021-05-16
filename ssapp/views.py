from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import * 
from django.contrib.auth.models import User
from .forms import * 
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
        register = 0
        for class_schedule in account.enrolled_class.all():
            register += class_schedule.course.credits
        total_courses = Course.objects.count()
        total_curriculum = Curriculum.objects.count()
        total_accounts = Account.objects.count()
        context = {"account": account, "courses": courses, 'register': register, 'majors': Curriculum.objects.all(), 'total_courses': total_courses, 'total_curriculum': total_curriculum, 'total_accounts': total_accounts}
        return render(self.request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        print(self.request.POST)
        account = Account.objects.filter(user=self.request.user)[0]
        user = self.request.user
        fname = self.request.POST['fname']
        lname = self.request.POST['lname']
        major = self.request.POST['major']
        print(fname, lname, major, account, user)
        if len(fname):
            user.first_name = fname
        if len(lname):
            user.last_name = lname
        if len(major):
            account.major = Curriculum.objects.get(pk=major)
        user.save()
        account.save()
        return redirect('ssapp:profile', pk=user)

class UserCurriculum(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/curriculum.html'
    
    def get(self, *args, **kwargs):
        account = Account.objects.filter(user=self.request.user)[0]
        ge_courses = account.major.courses.filter(category = 'General Education Courses')
        pro_courses = account.major.courses.exclude(category = 'General Education Courses')
        other_courses = account.completed_course.filter(category="Professional Courses").exclude(faculty=account.major.faculty)
        register = 0
        for class_schedule in account.enrolled_class.all():
            register += class_schedule.course.credits
            context = {"account": account, 'ge_courses': ge_courses, 'pro_courses': pro_courses, 'other_courses': other_courses, 'register': register}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.is_ajax and request.method == "POST":
            curr_acc = Account.objects.get(user=request.user)
            type = request.POST.get('type', 0)
            if type and type == 'unenroll' and request.POST.get('course_id', 0):
                course = Course.objects.get(pk=request.POST['course_id'])
                curr_acc.completed_course.remove(course)
                curr_acc.save()
            if type and type == 'complete':
                course = Course.objects.get(pk=request.POST['course_id'])
                curr_acc.completed_course.add(course)
                curr_acc.save()
        return JsonResponse({"instance": ""}, status=200)



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

class UserEnrollCourse(LoginRequiredMixin, generic.UpdateView):
    login_url = '/accounts/login'
    form_class = EnrollCourseForm
    template_name = 'ssapp/course.html'

    def get(self, *args, **kwargs):
        form = self.form_class()
        account = Account.objects.get(user=self.request.user)
        not_enroll_courses = account.major.courses.all()
        completed_courses = account.completed_course.all()
        not_enroll_courses = not_enroll_courses.difference(completed_courses)
        courses = account.enrolled_class.all()
        total = 0
        for one_class in courses:
            total += one_class.course.credits
        context = {"available_courses": not_enroll_courses, 'courses': courses, 'total': total}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            curr_acc = Account.objects.get(user=self.request.user)
            type = self.request.POST.get('type', 0)
            if type and type == 'unenroll' and self.request.POST.get('course_id', 0):
                course = Course.objects.get(pk=self.request.POST['course_id'])
                curr_acc.enrolled_class.remove(course.class_schedule)
                curr_acc.save()
            if type and type == 'enroll':
                courses = self.request.POST['courses']
                if courses.find(',') > 1:
                    courses_list = courses.split(',')
                    for course in courses_list:
                        curr_acc.enrolled_class.add(Course.objects.get(pk=course).class_schedule)
                else:
                    curr_acc.enrolled_class.add(Course.objects.get(pk=courses).class_schedule)
                curr_acc.save()
            return JsonResponse({"instance": ""}, status=200)


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
            action = self.request.POST['type']
            if action == 'add':
                form = self.form_class(self.request.POST)
                if form.is_valid():
                    instance = form.save()
                    ser_instance = serializers.serialize('json', [instance, ])
                    return JsonResponse({"instance": ser_instance}, status=200)
                else:
                    return JsonResponse({"error": ""}, status=400)
            if action == 'delete':
                course_pk = self.request.POST['curr_pk']
                if Curriculum.objects.filter(pk=course_pk).exists():
                    curr = Curriculum.objects.get(pk=course_pk)
                    curr.delete()
                return JsonResponse({"instance": ""}, status=200)

class AdminDetailCurriculum(LoginRequiredMixin, generic.UpdateView):
    login_url = '/accounts/login'
    template_name = 'ssapp/admin/detail_curriculum.html'
    form_class = UpdateCurriculumForm

    def get(self, *args, **kwargs):
        curr_curriculum = Curriculum.objects.filter(pk=self.kwargs['pk'])[0]
        courses = curr_curriculum.courses.all()
        ge_courses = curr_curriculum.courses.filter(category = 'General Education Courses')
        pro_courses = curr_curriculum.courses.exclude(category = 'General Education Courses')
        not_added_courses = Course.objects.filter(faculty=curr_curriculum.faculty).difference(courses)
        form = self.form_class()
        context = {"curriculum": curr_curriculum, 'ge_courses': ge_courses, 'pro_courses': pro_courses, 'difference_courses': not_added_courses, "form": form}
        return render(self.request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            curr = Curriculum.objects.filter(pk=self.kwargs['pk'])[0]
            courses = self.request.POST['courses']
            if courses.find(',') > 1:
                courses_list = courses.split(',')
                for course in courses_list:
                    curr.courses.add(Course.objects.get(pk=course))
                print("courses_list", courses_list)
            else:
                print("just one:", courses)
                curr.courses.add(Course.objects.get(pk=courses))
            curr.save()
            ser_instance = serializers.serialize('json', [])
            return JsonResponse({"instance": ser_instance}, status=200)

def auto_add_ge_courses(request, curr_id):
    if Curriculum.objects.filter(pk=curr_id).exists():
        curr = Curriculum.objects.get(pk=curr_id)
        ge_courses = Course.objects.filter(category='General Education Courses')
        for course in ge_courses:
            curr.courses.add(course)
        curr.save()
        return redirect('ssapp:admin_detail_curriculum', pk=curr_id)

def drop_course_from_curriculum(request, curr_id, course_id):
    if Course.objects.filter(pk=course_id).exists() and Curriculum.objects.filter(pk=curr_id).exists():
        course = Course.objects.get(pk=course_id)
        curr = Curriculum.objects.get(pk=curr_id)
        curr.courses.remove(course)
        curr.save()
        return redirect('ssapp:admin_detail_curriculum', pk=curr_id)

class AdminDashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'ssapp/admin/dashboard.html'
    login_url = '/accounts/login'

    def get(self, *args, **kwargs):
        context = {"all_courses": Course.objects.all(), 'all_faculty': Faculty.objects.all()}
        return render(self.request, self.template_name, context)


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
                id = self.request.POST['id']
                instance = form.save()
                cs = ClassSchedule.objects.create(course=Course.objects.get(pk=id), daytime=dict())
                cs.save()
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
        action = self.request.POST.get('action', '')
        if action != "reset_day":
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
                    if key in prev_class.daytime:
                        prev_class.daytime[day].append(session[day][0])
                        prev_class.daytime[day].append(session[day][1])
                    else:
                        prev_class.daytime[day] = session[day]
                prev_class.save()
        else:
            day = self.request.POST.get('day', '')
            curr_class = course_id.class_schedule
            curr_class.daytime.pop(day)
            curr_class.save()
        return JsonResponse({"instance": ""}, status=200)


