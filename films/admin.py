from django.contrib import admin
from .models import Genre, Film, Actor

# Register your models here.
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Actor)