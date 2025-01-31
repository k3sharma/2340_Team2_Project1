import os
from django.core.management.base import BaseCommand
from dashboard.models import Movie, Genre, MovieGenre
import os

class Command(BaseCommand):
    help = 'Delete everything from Movies, Genres, and MovieGenres tables'
    def handle(self, *args, **options):
        MovieGenre.objects.all().delete()
        Genre.objects.all().delete()
        Movie.objects.all().delete()
        image_dir = os.path.join('media', 'movies')
        if os.path.exists(image_dir):
            for filename in os.listdir(image_dir):
                file_path = os.path.join(image_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        self.stdout.write(self.style.SUCCESS('Successfully deleted all movies, genres, and movie genres.'))
        self.stdout.write("Movie table size: {}".format(Movie.objects.count()))
        self.stdout.write("Genre table size: {}".format(Genre.objects.count()))
        self.stdout.write("MovieGenre table size: {}".format(MovieGenre.objects.count()))
        self.stdout.write("Image directory size: {}".format(len(os.listdir(image_dir))))