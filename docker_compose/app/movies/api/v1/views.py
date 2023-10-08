from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmwork

ROLES = PersonFilmwork.Roles


class MoviesListApi(BaseListView):
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        query_set = self.model.objects.values().annotate(
            actors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__role=str(ROLES.ACTOR)),
                distinct=True
            ),
            directors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__role=str(ROLES.DIRECTOR)),
                distinct=True
            ),
            writers=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__role=str(ROLES.WRITER)),
                distinct=True
            ),
            genres=ArrayAgg('genres__name', distinct=True),
        )
        return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
