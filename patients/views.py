from distutils.command.clean import clean
from msilib.schema import ListView
from re import template
from django.shortcuts import render, redirect, reverse
from .models import Patient, Physician, FollowUp
from .forms import AssignPhysicianForm, FollowUpModelForm, PatientForm, PatientModelForm, CustomUserCreationForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from physicians.mixins import TeamleadRequiredMixin


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class PatientListView(LoginRequiredMixin, generic.ListView):
    template_name = "patients/patient_list.html"
    context_object_name = "patients"

    def get_queryset(self):
        user = self.request.user
        if user.is_teamlead:
            queryset = Patient.objects.filter(
                team=user.userprofile,
                physician__isnull=False
            )
        else:
            queryset = Patient.objects.filter(
                team=user.physician.team,
                physician__isnull=False
            )
            #filter for physican that is logged in
            queryset = queryset.filter(physician__user=user)
        
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(PatientListView, self).get_context_data(**kwargs)
        if user.is_teamlead:
            queryset = Patient.objects.filter(
                team=user.userprofile,
                physician__isnull=True
            )
            context.update({
                "unassigned_patients": queryset
            })
        return context


class PatientDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "patients/patient_detail.html"
    context_object_name = "patient"

    def get_queryset(self):
        user = self.request.user
        #intial queryset of the physician for the entire team
        if user.is_teamlead:
            queryset = Patient.objects.filter(team=user.userprofile)
        else:
            queryset = Patient.objects.filter(team=user.physician.team)
            #filter for physican that is logged in
            queryset = queryset.filter(physician__user=user)
        #print(Patient.objects.filter(team=user.userprofile))
        return queryset


class PatientCreateView(TeamleadRequiredMixin,generic.CreateView):
    template_name = "patients/patient_create.html"
    form_class =  PatientModelForm

    def get_success_url(self):
        return reverse("patients:patient-list")

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.team = self.request.user.userprofile
        patient.save()
        send_mail(
            subject="A patient has been created",
            message="Go to new site to see the new patient",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(PatientCreateView,self).form_valid(form)

class PatientUpdateView(TeamleadRequiredMixin,generic.UpdateView):
    template_name = "patients/patient_update.html"
    form_class =  PatientModelForm

    def get_queryset(self):
        user = self.request.user
        
        return Patient.objects.filter(team=user.userprofile)

    def get_success_url(self):
        return reverse("patients:patient-list")


class PatientDeleteView(TeamleadRequiredMixin,generic.DeleteView):
    template_name = "patients/patient_delete.html"
    
    def get_queryset(self):
        user = self.request.user
        
        return Patient.objects.filter(team=user.userprofile)

    def get_success_url(self):
        return reverse("patients:patient-list")

class AssignPhysicianView(TeamleadRequiredMixin, generic.FormView):
    template_name = "patients/assign_physician.html"
    form_class = AssignPhysicianForm

    def get_form_kwargs(self, **kwargs):
        kwargs =  super(AssignPhysicianView,self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request" : self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("patients:patient-list")

    def form_valid(self, form):
        physician = form.cleaned_data['physician']
        patient = Patient.objects.get(id=self.kwargs["pk"])
        patient.physician = physician
        patient.save()
        return super(AssignPhysicianView,self).form_valid(form)

class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "patients/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("patients:patient-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "patient": Patient.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        patient = Patient.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.patient = patient
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)

class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "patients/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_teamlead:
            queryset = FollowUp.objects.filter(patient__team=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(patient__team=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(patient__physician__user=user)
        return queryset

    def get_success_url(self):
        return reverse("patients:patient-detail", kwargs={"pk": self.get_object().patient.id})

class FollowUpDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "patients/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("patients:patient-detail", kwargs={"pk": followup.patient.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_teamlead:
            queryset = FollowUp.objects.filter(patient__team=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(patient__team=user.physician.team)
            # filter for the agent that is logged in
            queryset = queryset.filter(patient__physician__user=user)
        return queryset

""" def patient_update(request, pk):
    patient = Patient.objects.get(id=pk)
    form = PatientForm()
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            patient.first_name = first_name
            patient.last_name = last_name
            patient.age = age
            patient.save()
            return redirect("/patients")
    context = {
        "form" : form,
        "patient" : patient
    }
    return render(request, "patients/patient_update.html",context)
 """