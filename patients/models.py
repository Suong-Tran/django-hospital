from unicodedata import category
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_teamlead = models.BooleanField(default=True)
    is_physician = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    team = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    physician = models.ForeignKey('Physician', null=True, blank=True,on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def handle_upload_follow_ups(instance, filename):
    return f"patient_followups/patient_{instance.patient.pk}/{filename}"


class FollowUp(models.Model):
    patient = models.ForeignKey(Patient, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name}"

class Physician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    department = models.ForeignKey("Department", related_name="physicians" ,null=True, blank=True,on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Department(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    team_lead = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)