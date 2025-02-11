from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import CustomPasswordResetView
from .views import ResetPasswordView
from .views import DebugPasswordResetView

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),


    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    # path('password-reset/', DebugPasswordResetView.as_view(), name='password_reset'),

]