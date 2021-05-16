from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{}".format(self.name)

class Curriculum(models.Model):
    name = models.CharField(max_length=50, unique=True)
    total_credits = models.PositiveSmallIntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', blank=True, related_name="curriculum")

    def __str__(self):
        return "{}".format(self.name)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    major = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='major', null=False)
    enrolled_class = models.ManyToManyField('ClassSchedule', blank=True, related_name="enrolled_class") 
    completed_course = models.ManyToManyField('Course', blank=True, related_name="completed_courses") 
    earned_credits = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return "Username: {}".format(self.user.username)

class Course(models.Model):
    id =  models.CharField(max_length=10, primary_key=True)
    name =  models.CharField(max_length=50)
    credits = models.PositiveSmallIntegerField(default=3)
    category = models.CharField(
        choices = [
            ("General Education Courses", "General Education Courses"),
            ("Professional Courses", "Professional Courses"),
        ], max_length=30, default="Professional Courses"
    ) 
    faculty = models.ManyToManyField('Faculty', blank=True, related_name="courses")
     
    def __str__(self):
        return f"{self.id} {self.name} ({self.credits})"


class ClassSchedule(models.Model): 
    course = models.OneToOneField(Course, primary_key=True, on_delete=models.CASCADE, related_name='class_schedule') 
    availability = models.BooleanField(default=False)
    daytime = PickledObjectField(default=dict())

    def __str__(self):
        return "{}: {}".format(self.course.id, self.course.name)

class Class(models.Model): 
    id = models.CharField(max_length=10, primary_key=True)
    availability = models.BooleanField(default=False)
    daytime = PickledObjectField(default=dict())

    def __str__(self):
        return "{}".format(self.id)
