import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('actor')
        verbose_name_plural = _('actors')


class Genre(UUIDMixin, TimeStampedMixin):

    def __str__(self):
        return self.name

    name = models.CharField(_('name'), max_length=255)

    description = models.TextField(_('description'), null=True, blank=True,)

    class Meta:

        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['genre_id', 'film_work_id'],
                name='film_work_genre_idx',
            ),
        ]


class PersonFilmwork(UUIDMixin):

    class Roles(models.TextChoices):
        ACTOR = 'actor'
        DIRECTOR = 'director'
        WRITER = 'writer'

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'person_id', 'film_work_id'],
                name='film_work_person_idx_role',
            ),
        ]


class FilmWork(UUIDMixin, TimeStampedMixin):
    genres = models.ManyToManyField(Genre, through=GenreFilmwork)
    persons = models.ManyToManyField(Person, through=PersonFilmwork)

    def __str__(self):
        return self.title

    def validate_interval(rating_value):
        min_value = 1.0
        max_value = 10.0
        if rating_value < min_value or rating_value > max_value:
            raise ValidationError(
                _('Rating must be in range between [{0}, {1}]'.format(
                    min_value,
                    max_value,
                ),
                ),
                params={'value': rating_value},
            )

    class MoviesType(models.TextChoices):
        MOVIES = _('movie')
        TV_SHOW = _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)
    creation_date = models.DateField(_('creation_date'), null=True, blank=True)
    rating = models.FloatField(
        _('rating'),
        validators=[validate_interval],
        null=True,
        blank=True,
    )
    type = models.CharField(
        _('type'),
        choices=MoviesType.choices,
        max_length=7,
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('piece of art')
        verbose_name_plural = _('pieces of arts')
