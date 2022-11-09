from django.contrib import admin

from mListy.movie.models import MovieDB


@admin.register(MovieDB)
class MovieDBAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'name', 'poster', 'description', 'duration', 'genres', 'average_grade', 'actors',
                    'roles', 'production_companies', 'language', 'imdb_link', 'budget', 'release_date', 'status']
