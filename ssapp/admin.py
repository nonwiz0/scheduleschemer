from django.contrib import admin
from .models import Class, Account, Curriculum, Course, Program, CourseCategory, Faculty

# Register your models here.
admin.site.register(Class)
admin.site.register(Account)
admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(Program)
admin.site.register(CourseCategory)
admin.site.register(Faculty)
