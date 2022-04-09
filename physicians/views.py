from audioop import reverse
import random as rand
from re import template
from urllib import request
from django.forms import GenericIPAddressField
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from patients.models import Department, Physician
from .forms import PhysicianDepartmentUpdateForm, PhysicianModelForm
from .mixins import TeamleadRequiredMixin
from django.core.mail import send_mail

class PhysicianListView(TeamleadRequiredMixin, generic.ListView):
    template_name = "physicians/physician_list.html"

    def get_queryset(self):
        team = self.request.user.userprofile
        return Physician.objects.filter(team=team)


class PhysicianCreateView(TeamleadRequiredMixin, generic.CreateView):
    template_name = "physicians/physician_create.html"
    form_class = PhysicianModelForm

    def get_success_url(self):
        return reverse("physicians:physician-list")
    
    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_physician = True
        user.is_teamlead = False
        user.set_password(f"{rand.randint(0,100000)}")
        user.save()
        Physician.objects.create(
            user=user,
            team=self.request.user.userprofile,

        )

        send_mail(
            subject="This is not a scam. You are now a physician!!!",
            message="Congratulation. You are now a physician of Medicare Hospital.",
            from_email="admin@test.com",
            recipient_list=[
                user.email
            ]
        )
        # physician.team = self.request.user.userprofile
        # physician.save()
        return super(PhysicianCreateView,self).form_valid(form)

class PhysicianDetailView(TeamleadRequiredMixin, generic.DetailView):
    template_name = "physicians/physician_detail.html"
    context_object_name = "physician"

    def get_queryset(self):
        user = self.request.user
        queryset = Physician.objects.filter(team=user.userprofile)
        queryset = queryset.filter(user=user)  
        
        return queryset

class PhysicianUpdateView(TeamleadRequiredMixin, generic.UpdateView):
    template_name = "physicians/physician_update.html"
    form_class = PhysicianModelForm

    def get_success_url(self):
        return reverse("physicians:physician-list")

    def get_queryset(self):
        user = self.request.user
        queryset = Physician.objects.filter(team=user.userprofile)
        queryset = queryset.filter(user=user) 
        print(queryset)
        return queryset
    
class PhysicianDeleteView(TeamleadRequiredMixin, generic.DeleteView):
    template_name = "physicians/physician_delete.html"
    context_object_name = "physician"

    def get_queryset(self):
        team = self.request.user.userprofile
        return Physician.objects.filter(team=team)

    def get_success_url(self):
        return reverse("physicians:physician-list")

class DepartmentListView(LoginRequiredMixin, generic.ListView):
    template_name = "physicians/department_list.html"
    context_object_name = "departments"

    def get_context_data(self, **kwargs):
        context = super(DepartmentListView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_teamlead:
            queryset =Physician.objects.filter(
                team=user.userprofile,
            )
        else:
            queryset = Physician.objects.filter(
                team=user.physician.team,
            )
        context.update({
            "unassigned_physicians" : queryset.filter(department__isnull=True),
            "unassigned_physicians_count" : queryset.filter(department__isnull=True).count(),
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_teamlead:
            queryset = Department.objects.filter(
                team_lead=user.userprofile,
            )
        else:
            queryset = Department.objects.filter(
                team_lead=user.team,
            )
        
        return queryset

class DepartmentDetailView(LoginRequiredMixin, generic.DeleteView):

    template_name = "physicians/department_detail.html"
    context_object_name = "department"

    def get_queryset(self):
        user = self.request.user
        if user.is_teamlead:
            queryset = Department.objects.filter(
                team_lead=user.userprofile,
            )
        else:
            queryset = Department.objects.filter(
                team_lead=user.team,
            )
        
        return queryset

class DepartmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "physicians/physician_department_update.html"
    form_class = PhysicianDepartmentUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_teamlead:
            queryset = Physician.objects.filter(team=user.userprofile)
        else:
            queryset = Physician.objects.filter(team=user.team)
            queryset = queryset.filter(user=user)
        return queryset

    def get_success_url(self):
        return reverse("physicians:physician-detail", kwargs={"pk":self.get_object().id})