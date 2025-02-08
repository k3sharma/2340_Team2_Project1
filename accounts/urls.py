from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import ResetPasswordView
from .views import DebugPasswordResetView

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    # path('forgot-password.html', views.forgot_password, name='accounts.forgot_password'),

    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')), # password reset

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('test-email/', test_email, name='test_email'),
    # path('password-reset/', DebugPasswordResetView.as_view(), name='password_reset'),

]