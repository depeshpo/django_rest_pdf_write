from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('author'):
            return ['author']
        return super(CustomSearchFilter, self).get_search_fields(view, request)
