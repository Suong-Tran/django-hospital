from django.urls import path
from .views import (
    AssignPhysicianView, PatientListView,
    PatientDetailView, PatientCreateView, PatientUpdateView,
    PatientDeleteView, FollowUpCreateView, FollowUpUpdateView, FollowUpDeleteView
)
app_name = "patients"

urlpatterns = [
    path('', PatientListView.as_view(), name="patient-list"),
    path('<int:pk>/', PatientDetailView.as_view(), name="patient-detail"),
    path('create/', PatientCreateView.as_view(), name="patient-create"),
    path('<int:pk>/update/', PatientUpdateView.as_view(), name="patient-update"),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name="patient-delete"),
    path('<int:pk>/assign-physician/',AssignPhysicianView.as_view(),name="assign-physician"),
    path('<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='patient-followup-create'),
    path('followups/<int:pk>/', FollowUpUpdateView.as_view(), name='patient-followup-update'),
    path('followups/<int:pk>/delete/', FollowUpDeleteView.as_view(), name='patient-followup-delete'),
]