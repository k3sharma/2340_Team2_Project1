from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.movie_dashboard, name='movie_dashboard'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('<int:movie_id>/review/create/', views.create_review, name='create_review'),
    path('<int:movie_id>/review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('<int:movie_id>/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)