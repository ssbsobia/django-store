from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid

from .models import AppUser, PasswordResetToken
from .forms import PasswordResetForm, SetNewPasswordForm, RegistrationForm


class RegistrationView(FormView):
    """View to handle user registration"""
    form_class = RegistrationForm
    template_name = 'account/registration.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            'Registration successful! Please login with your credentials.'
        )
        return super().form_valid(form)


class AppUserLoginView(auth_views.LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(1209600)  # 2 weeks
        else:
            self.request.session.set_expiry(0)  # browser close
        return super().form_valid(form)


def logout_view(request):
    auth_logout(request)
    return redirect('home')


class PasswordResetView(FormView):
    """View to request password reset"""
    form_class = PasswordResetForm
    template_name = 'account/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = AppUser.objects.get(email=email)
        
        # Invalidate old tokens
        user.password_reset_tokens.filter(is_used=False).update(is_used=True)
        
        # Create new token
        token = PasswordResetToken.objects.create(user=user)
        
        # Send email
        reset_link = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', kwargs={'token': str(token.token)})
        )
        
        # Render email template
        email_context = {
            'user': user,
            'reset_link': reset_link,
            'site_name': 'Mobile Store',
        }
        
        html_message = render_to_string('account/password_reset_email.html', email_context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Password Reset Request - Mobile Store',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        messages.success(
            self.request,
            f'Password reset link has been sent to {email}'
        )
        return super().form_valid(form)


class PasswordResetConfirmView(FormView):
    """View to reset password with token"""
    form_class = SetNewPasswordForm
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_success')

    def dispatch(self, request, *args, **kwargs):
        self.token_obj = None
        token = kwargs.get('token')
        
        try:
            self.token_obj = PasswordResetToken.objects.get(
                token=token,
                is_used=False
            )
            
            # Check if token is expired
            if timezone.now() - self.token_obj.created_at > timedelta(
                seconds=settings.PASSWORD_RESET_TIMEOUT
            ):
                messages.error(request, 'Password reset link has expired.')
                return redirect('password_reset')
                
        except PasswordResetToken.DoesNotExist:
            messages.error(request, 'Invalid or expired reset link.')
            return redirect('password_reset')
        
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.token_obj.user
        return kwargs

    def form_valid(self, form):
        user = self.token_obj.user
        user.set_password(form.cleaned_data['new_password1'])
        user.save()
        
        # Mark token as used
        self.token_obj.is_used = True
        self.token_obj.save()
        
        messages.success(self.request, 'Your password has been reset successfully. You can now login.')
        return super().form_valid(form)


class PasswordResetDoneView(TemplateView):
    """View after password reset request is sent"""
    template_name = 'account/password_reset_done.html'


class PasswordResetSuccessView(TemplateView):
    """View after successful password reset"""
    template_name = 'account/password_reset_success.html'

