from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmwork

ROLES = PersonFilmwork.Roles
PAGINATE_BY = 50


class MoviesApiMixin(BaseListView):
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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = {
    #         'results': list(self.get_queryset()),
    #     }
    #     return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = PAGINATE_BY

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            MoviesListApi.paginate_by
        )

        context = {
            'count': paginator.count,
            "total_pages": paginator.num_pages,
            "prev":
                page.previous_page_number() if page.has_previous() else None,
            "next":
                page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }

        return context
