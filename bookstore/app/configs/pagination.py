from typing import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = 'Page'
    page_size_query_param = 'Limit'
    page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'Pagination_Data': {
                # 'Current_Page': int(self.request.query_params.get('Page', 1)),
                # 'Current_Page': int(self.request.GET.get('Page', 1)),
                'Current_Page': self.page.number,
                'Max_Data_Per_Page': self.page.paginator.per_page,
                'Max_Page': self.page.paginator.num_pages,
                'Total_All_Data': self.page.paginator.count,
            },
            'List_Data': data,
        })
