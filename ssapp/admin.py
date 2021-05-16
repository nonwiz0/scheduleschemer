from django.contrib import admin
from .models import Account, Curriculum, Course, Faculty, ClassSchedule

# Register your models here.
admin.site.register(Account)
admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(ClassSchedule)
