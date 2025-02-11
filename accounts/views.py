from django.shortcuts import render
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.core.mail import send_mail
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)


from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'email/user_reset_password.html'
    subject_template_name = 'email/user_reset_password.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('movie_dashboard')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'email/user_reset_password.html'
    subject_template_name = 'email/user_reset_password.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('movie_dashboard')


class DebugPasswordResetView(PasswordResetView):
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"🚩 Incoming request: {request.method} to {request.path}")
        print(f"🚩 Incoming request: {request.method} to {request.path}")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        logger.info("✅ Form is valid. Sending password reset email.")
        print("✅ Form is valid. Sending password reset email.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(f"❌ Form is invalid: {form.errors}")
        print(f"❌ Form is invalid: {form.errors}")
        return super().form_invalid(form)

# for logout web request/response
@login_required
def logout(request):
    auth_logout(request)
    return redirect('http://127.0.0.1:8000/')


# for login web request/response
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('http://127.0.0.1:8000/')

# for signup web request/response
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            auth_login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})
