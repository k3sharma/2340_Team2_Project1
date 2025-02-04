from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.movie_dashboard, name='movie_dashboard'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('about/', views.about, name='about'),
<<<<<<< HEAD
<<<<<<< HEAD

=======
    path('search/', views.search, name='search'),
>>>>>>> b882f04 (Searching feature implemented as well as minor aesthetic changes.)
=======
    path('<int:movie_id>/review/create/', views.create_review, name='create_review'),
>>>>>>> e3ec4dc (Commiting reviews feature)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)