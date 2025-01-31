from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    discription = models.TextField()
    image = models.URLField()
    release_date = models.DateField()
    genres = models.ManyToManyField("Genre", related_name="movies")

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name