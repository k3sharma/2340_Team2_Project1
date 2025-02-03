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

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'email/user_reset_password.html'
    subject_template_name = 'email/user_reset_password.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('movie_dashboard')
#
# def test_email(request):
#     try:
#         send_mail(
#             'Django Email Test',
#             'This is a test email from Django via SendGrid.',
#             'kush3sharma@gmail.com',  # Must match the verified sender
#             ['kush3sharma@gmail.com'],  # Your email to receive the test
#             fail_silently=False,
#         )
#         return HttpResponse('Test email sent successfully!')
#     except Exception as e:
#         return HttpResponse(f'Error: {e}')
#
# class DebugPasswordResetView(PasswordResetView):
#     def form_valid(self, form):
#         print("Password reset form is valid.")  # Debugging log
#         response = super().form_valid(form)
#         print("Password reset email should be sent.")  # Debugging log
#         return response
#
#     def form_invalid(self, form):
#         print("Form is invalid:", form.errors)  # Debugging log
#         return super().form_invalid(form)
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
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})

