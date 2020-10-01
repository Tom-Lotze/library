from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=200, default='', unique=True)
    url = models.CharField(max_length=200, default='')

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(max_length=200, default='', unique=True)

    class Meta:
        ordering = ['genre']

    def __str__(self):
        return self.genre




class Film(models.Model):
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    # IMDB link
    link = models.CharField(max_length=1000, default='')
    title = models.CharField(max_length=200, default='', unique=True)
    isSerie = models.BooleanField(default=False)
    nrEpisodes = models.IntegerField(default=0)
    CurrEpisode = models.IntegerField(default=0)

    description = models.CharField(max_length=5000, default='')
    imageURL =  models.CharField(max_length=200, default='')

    director = models.CharField(max_length=200, default='')
    releaseDate = models.DateTimeField('Date published', default=timezone.now)

    # Starring
    starring = models.ManyToManyField(Actor)

    duration = models.DurationField(default=timedelta)

    rating = models.DecimalField(default=0, decimal_places = 1, max_digits=3
        )

    metascore = models.IntegerField(default=0, validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    ownRating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)
        ])

    # Genre one to many
    genre = models.ManyToManyField(Genre)

    # On which list?
    statuschoices = [
    ('TODO', 'On watchlist'),
    ('SEEN', 'Seen')]

    status = models.CharField(
        max_length=4,
        choices=statuschoices,
        default='TODO')

    favorite = models.BooleanField(default=False)
    review = models.CharField(max_length=1500, default='')

    class Meta:
        ordering = ['-modified']


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()

        return super(Film, self).save(*args, **kwargs)