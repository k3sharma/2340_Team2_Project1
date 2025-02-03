from django.db import models
from django.urls import reverse
import os

def movie_image_path(instance, filename):
    return os.path.join('movies', f"{str(instance.id)}_{instance.title.replace(' ', '_')}.jpg")

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=movie_image_path)
    release_date = models.DateField()
    price = 16

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Genre(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} - {self.genre.name}"