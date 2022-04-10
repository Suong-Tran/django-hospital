from urllib import request
from django import forms
from .models import FollowUp, Patient, Physician, User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

class PatientModelForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = (
            'first_name',
            'last_name',
            'age',
            'email',
            'phone_number',
            'physician',
        )

class PatientForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

class AssignPhysicianForm(forms.Form):
    physician = forms.ModelChoiceField(queryset=Physician.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        physicians = Physician.objects.filter(team=request.user.userprofile)
        super(AssignPhysicianForm,self).__init__(*args, **kwargs)
        self.fields["physician"].queryset = physicians

class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'message',
            'file'
        )