from django.forms import ModelForm
from django import forms
from .models import Teacher_login_informa, Student_login_informatn


class chg_pass(ModelForm):
    class Meta:
        model = Teacher_login_informa
        fields = ['Teacher_pass']

class chg_pass_stu(ModelForm):
    class Meta:
        model = Student_login_informatn
        fields = ['Student_pass']


