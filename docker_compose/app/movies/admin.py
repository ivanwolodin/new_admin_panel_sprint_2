from django.contrib import admin
from .models import (
    FilmWork,
    Genre,
    GenreFilmwork,
    Person,
    PersonFilmwork,
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person', )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('person', )


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating')

    # Фильтрация в списке
    list_filter = ('type', 'rating')

    # Поиск по полям
    search_fields = ('title', 'description', 'id')
