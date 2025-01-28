import requests
from django.shortcuts import render

def movie_dashboard(request):
    api_url = "https://api.themoviedb.org/3/movie/popular"
    api_key = "8900ca2afeda851652760fdb0cf3690c"
    params = {"api_key": api_key, "language": "en-US", "page": 1}

    response = requests.get(api_url, params=params)
    movies = response.json().get("results", []) if response.status_code == 200 else []

    context = {
        "movies": movies,
        "image_base_url": "https://image.tmdb.org/t/p/w500/",
    }
    return render(request, "dashboard/movies.html", context)