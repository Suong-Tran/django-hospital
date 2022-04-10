from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from patients.models import Department, Physician

User = get_user_model()

class PhysicianModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )

class PhysicianDepartmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Physician
        fields = (
            'department',
        )

class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'abbreviation',
            'description',
        )