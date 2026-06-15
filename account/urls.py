from django.urls import path
from .views import (
    RegistrationView,
    AppUserLoginView, 
    logout_view,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetSuccessView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-success/', PasswordResetSuccessView.as_view(), name='password_reset_success'),
]
