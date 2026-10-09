from rest_framework.pagination import PageNumberPagination

class CustomReportPaginator(PageNumberPagination):
    page_size = 100
    max_page_size = 150
    page_size_query_param = 'page_size'

class CustomUnitReportPaginator(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'

class CustomAfrReportPaginator(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'