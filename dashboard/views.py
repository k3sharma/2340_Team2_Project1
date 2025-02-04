import requests
from django.shortcuts import render, get_object_or_404, redirect
from dashboard.models import Movie, Genre, MovieGenre, Review
from django.contrib.auth.decorators import login_required
import logging
def movie_dashboard(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'dashboard/movies.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)

    # FIXME: Delete when rating is implemented
    movie.rating =5.0
    user = request.user
    associated_genres = Genre.objects.filter(moviegenre__movie=movie)
    context = {
        'movie': movie,
        'genres': associated_genres,
        'reviews': reviews
    }
    return render(request, 'dashboard/movie_detail.html', context)


def about(request):
    return render(request, 'dashboard/about.html')

<<<<<<< HEAD
def search(request):
    query = request.GET.get('search-input')
    filtered_movies = Movie.objects.filter(title__icontains=query) if query else Movie.objects.all()
    return render(request, 'dashboard/search.html', {'filtered_movies': filtered_movies})
=======
@login_required
def create_review(request, movie_id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=movie_id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movie_detail', movie_id=movie_id)
    else:
        return redirect('movie_detail', movie_id=movie_id)
>>>>>>> e3ec4dc (Commiting reviews feature)
