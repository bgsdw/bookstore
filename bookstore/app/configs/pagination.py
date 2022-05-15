from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = 'Page'
    page_size_query_param = 'Limit'
