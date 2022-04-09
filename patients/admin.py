from django.contrib import admin

from .models import Department, User, Patient, Physician, UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Patient)
admin.site.register(Physician)
admin.site.register(Department)