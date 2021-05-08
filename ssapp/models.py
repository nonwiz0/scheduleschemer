from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=5)

    def __str__(self):
        return "{}".format(self.name)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    major = models.CharField(
        choices=[
            ("Information Technology", "IT"), 
            ("Accounting", "ACCT"), 
            ("TESOL", "TESOL"),
            ("Management", "MGNT"),
            ("Teaching", "TEACH"),
            ("Christian Studies", "CS"),
            ("Bioscience", "BIO"),
            ("Public Health", "PH"),
            ("MedTech", "MT"),
            ("English as a Second Language", "ESL"),
            ("Nursing", "NURS")
        ], max_length=50, default="English as a Second Language"
    )
    faculty = models.CharField(
        choices=[
            ("Arts & Humanities", "FAH"),
            ("Business Administration", "FBA"),
            ("Education", "FED"),
            ("Religious Studies", "FRS"),
            ("Science", "FOS"),
            ("Information Technology", "FIT"),
            ("Mission Faculty of Nursing", "MFN"),
        ], max_length=50, default="Arts & Humanities"
    )
    enrolled_course = PickledObjectField(default=dict())
    completed_course = PickledObjectField(default=dict())

    def __str__(self):
        return "Username: {}, Major: {}".format(self.user.username, self.major)

class Program(models.Model):
    name = models.CharField(max_length=50)
    total_credits = models.PositiveSmallIntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    """faculty = models.CharField(
        choices=[
            ("Arts & Humanities", "Arts & Humanities"),
            ("Business Administration", "Business Administration"),
            ("Education", "Education"),
            ("Religious Studies", "Religious Studies"),
            ("Science", "Science"),
            ("Information Technology", "Information Technology"),
            ("Mission Faculty of Nursing", "Mission Faculty of Nursing"),
        ], max_length=50, default="Arts & Humanities"
    )"""

    def __str__(self):
        return "{}".format(self.name)

 
class Curriculum(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    total_credits = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{}".format(self.name)

class CourseCategory(models.Model):
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{}".format(self.type)
    
class Course(models.Model):
    id =  models.CharField(max_length=10, primary_key=True)
    name =  models.CharField(max_length=50)
    credits = models.PositiveSmallIntegerField()
    category = models.ManyToManyField(CourseCategory) 


class Class(models.Model): 
    id = models.CharField(max_length=10, primary_key=True)
    availability = models.BooleanField(default=False)
    daytime = PickledObjectField()

    def __str__(self):
        return "name: {}, daytime: {}".format(self.id, self.daytime)
