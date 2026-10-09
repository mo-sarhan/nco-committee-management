from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
import math

class CustomPaginator(PageNumberPagination):
    # page_size = 20
    # max_page_size = 50
    # page_size_query_param = 'page_size'

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size =50 

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        total_pages = math.ceil(total_items / page_size)

        return Response({
            "count": total_items,
            "page": self.page.number,
            "page_size": page_size,
            "total_pages": total_pages,
            "previous": self.get_previous_link(),
            "next": self.get_next_link(),
            "last": self.get_last_link(),
            "results": data,
        })

    def get_last_link(self):
        if not self.page.paginator.num_pages:
            return None

        url = self.request.build_absolute_uri()
        return replace_query_param(
            url,
            self.page_query_param,
            self.page.paginator.num_pages
        )