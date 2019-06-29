from django.db import models

# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"
        ordering = ('name', )


class Movie(models.Model):
    title = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor)
    year = models.IntegerField()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ('title',)

    def __str__(self):
        return self.title
