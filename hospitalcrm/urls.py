from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from hospitalcrm.settings import STATIC_ROOT, STATIC_URL
from patients.views import LandingPageView, SignupView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, 
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="landing-page"),
    path('patients/',include('patients.urls', namespace="patients")),
    path('physicians/',include('physicians.urls', namespace="physicians")),
    path('login/', LoginView.as_view(),name='login'),
    path('logut/',LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name="signup"),

    path('reset-password/',PasswordResetView.as_view(), name="reset-password"),
    path('password-reset-done/',PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)