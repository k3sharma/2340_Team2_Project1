import os
import requests
from django.core.management.base import BaseCommand
from dashboard.models import Movie, Genre, MovieGenre
from django.core.files import File
from tempfile import NamedTemporaryFile

TMDB_API_KEY = '8900ca2afeda851652760fdb0cf3690c'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
MOVIE_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

class Command(BaseCommand):
    help = 'Scrape 300 movies and their genres from TMDB'

    def handle(self, *args, **kwargs):
        self.scrape_movies_and_save()

    def scrape_movies_and_save(self):
        genres = self.get_genres()

        movie_count = 0
        page = 1

        while movie_count < 300:
            response = requests.get(f'{TMDB_BASE_URL}/movie/popular', params={
                'api_key': TMDB_API_KEY,
                'language': 'en-US',
                'page': page
            }, verify=False)
            movies_data = response.json().get('results', [])
            # print(f"Page {page} - Movies fetched: {len(movies_data)}")
            if not movies_data:
                break

            for movie_data in movies_data:
                if movie_count >= 300:
                    break
                self.save_movie(movie_data, genres)
                movie_count += 1
            page += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully added {movie_count} movies."))

    def get_genres(self):
        response = requests.get(f'{TMDB_BASE_URL}/genre/movie/list', params={
            'api_key': TMDB_API_KEY,
            'language': 'en-US'
        }, verify=False)
        genre_data = response.json().get('genres', [])
        genre_dict = {}

        for genre in genre_data:
            genre_obj, _ = Genre.objects.get_or_create(id=genre['id'], name=genre['name'])
            genre_dict[genre['id']] = genre_obj

        return genre_dict

    def save_movie(self, movie_data, genres):
        description = movie_data.get('overview', 'No description available')

        image_url = f"{MOVIE_IMAGE_BASE_URL}{movie_data['poster_path']}" if movie_data.get('poster_path') else None
        movie = Movie(
            id=movie_data['id'],
            title=movie_data['title'],
            description=description,
            release_date=movie_data.get('release_date', None)
        )

        if image_url:
            response = requests.get(image_url, verify=False)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                movie.image.save(os.path.basename(image_url), File(img_temp))

        movie.save()

        for genre_id in movie_data.get('genre_ids', []):
            genre = genres.get(genre_id)
            if genre:
                MovieGenre.objects.get_or_create(movie=movie, genre=genre)