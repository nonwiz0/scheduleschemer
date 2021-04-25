from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id =  models.CharField(max_length=10, primary_key=True)
    major = models.CharField(max_length=50)
    minor = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)
    enrolled_course = PickledObjectField()

    def __str__(self):
        return "ID: {}, Username: {}, Major: {}".format(self.id, self.user.username, self.major)

class Course(models.Model):
    id =  models.CharField(max_length=10, primary_key=True)
    name =  models.CharField(max_length=50)
    credit = models.PositiveSmallIntegerField()
    lecturer = models.CharField(max_length=50)
    major = models.CharField(max_length=50)


class Class(models.Model):
    # id = models.ForeignKey(Course, on_delete=models.CASCADE, primary_key=True)
    # DayTime = {“Mon”:  [“Time
    # start”, “Time
    # end”], “Tues”: [“Time
    # start”, “Time
    # end”]}
    availability = models.BooleanField(default=False)
    daytime = PickledObjectField()

    def __str__(self):
        return "Day time: {}".format(self.daytime)