'''
Pagination classes
'''
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1


class StandardResultsSetPagination(PageNumberPagination):
    """
    standard page returns <= 100 objects
    """

    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page = DEFAULT_PAGE

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),  # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })

