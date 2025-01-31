import requests
from django.shortcuts import render, get_object_or_404
from dashboard.models import Movie, Genre, MovieGenre
import logging
def movie_dashboard(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'dashboard/movies.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # FIXME: Delete when rating is implemented
    movie.rating =5.0
    user = request.user
    associated_genres = Genre.objects.filter(moviegenre__movie=movie)
    context = {
        'movie': movie,
        'genres': associated_genres
    }
    return render(request, 'dashboard/movie_detail.html', context)


def about(request):
    return render(request, 'dashboard/about.html')