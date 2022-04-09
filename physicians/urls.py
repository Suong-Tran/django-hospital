from django.urls import path

from patients.models import Department
from physicians.forms import PhysicianDepartmentUpdateForm
from .views import (
    DepartmentDetailView, DepartmentListView, DepartmentUpdateView, PhysicianCreateView, PhysicianDeleteView, PhysicianDetailView,
     PhysicianListView, PhysicianUpdateView
)

app_name = 'physicians'

urlpatterns = [
    path('',PhysicianListView.as_view(),name="physician-list"),
    path('create/', PhysicianCreateView.as_view(), name="physician-create"),
    path('<int:pk>/', PhysicianDetailView.as_view(), name="physician-detail"),
    path('<int:pk>/update/', PhysicianUpdateView.as_view(), name="physician-update"),
    path('<int:pk>/delete/', PhysicianDeleteView.as_view(), name="physician-delete"),
    path("departments/",DepartmentListView.as_view(), name="department-list"),
    path("departments/<int:pk>/",DepartmentDetailView.as_view(),name="department-detail"),
    path('<int:pk>/update-department/',DepartmentUpdateView.as_view(),name="physician-department-update")
]