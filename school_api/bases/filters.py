from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES
from rest_framework import exceptions
from rest_framework.filters import SearchFilter

SEARCH_MIN_LENGTH = 3


class CustomSearchFilter(SearchFilter):
    def check_min_length(self, request, view):
        min_length = getattr(view, "search_min_length", SEARCH_MIN_LENGTH)
        search_terms = list("".join(self.get_search_terms(request)))

        if not search_terms:
            return

        if len(search_terms) < min_length:
            raise exceptions.NotAcceptable("Invalid search, minimum length is %s" % min_length)

    def filter_queryset(self, request, queryset, view):
        self.check_min_length(request, view)
        return super().filter_queryset(request, queryset, view)


class MultipleChoiceFilter(filters.CharFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lookup_expr = "in"

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        value = value.split(",")

        if self.distinct:
            qs = qs.distinct()
        lookup = "%s__%s" % (self.field_name, self.lookup_expr)
        qs = self.get_method(qs)(**{lookup: value})
        return qs
