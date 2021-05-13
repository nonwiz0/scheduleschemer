from .models import Class, Account, Curriculum, Course
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CurriculumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CurriculumForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 

    class Meta:
        model = Curriculum
        fields = ('name', 'total_credits', 'faculty')
 

class UpdateCurriculumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateCurriculumForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 

    class Meta:
        model = Curriculum
        fields = ['courses', ]
 
class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 

    class Meta:
        model = Course 
        fields = ('id', 'name', 'credits', 'category')

class EnrollCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnrollCourseForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            }) 

    class Meta:
        model = Account 
        fields = ['enrolled_class',]


