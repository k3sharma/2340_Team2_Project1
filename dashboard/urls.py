from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_dashboard, name='movie_dashboard'),
]