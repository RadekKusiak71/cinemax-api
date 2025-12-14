from django.contrib import admin

from movies.models import Director, Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'director','original_language', 'age_restriction')
    list_select_related = ('director', 'original_language')
    search_fields = ('title', 'director__first_name', 'director__last_name', 'original_language__name')
    list_filter = ('release_year', 'age_restriction', 'genres', 'original_language', 'director')