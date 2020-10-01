from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200, default="")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    link = models.CharField(max_length=1000, default='')
    title = models.CharField(max_length=200, default='', unique=True)
    description = models.CharField(max_length=5000, default='')
    image_url =  models.CharField(max_length=200, default='')
    isbn =  models.CharField(max_length=20, default='')

    # authors = models.ManyToManyField(Author)
    authors = models.CharField(max_length=200, default='')
    publication_date = models.DateTimeField('Date published', default=timezone.now)



    languagechoices = [
        ('EN', 'English'),
        ('NL', 'Nederlands')]
    language = models.CharField(
        max_length=2,
        choices=languagechoices,
        default='NL')

    rating = models.IntegerField(default=0, validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])

    nrPages = models.IntegerField(default=0, validators=[
            MaxValueValidator(2000),
            MinValueValidator(0)
        ])

    # On which list?
    statuschoices = [
    ('WISH', 'On wishlist'),
    ('TODO', 'To read'),
    ('CURR', 'Currently reading'),
    ('READ', 'Read')]

    status = models.CharField(
        max_length=4,
        choices=statuschoices,
        default='WISH')

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

        return super(Book, self).save(*args, **kwargs)




