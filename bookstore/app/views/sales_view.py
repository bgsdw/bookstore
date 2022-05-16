from datetime import datetime

from bookstore.app.models import Sales
from bookstore.app.serializers.sales_serializer import (SalesAddSerializer,
                                                        SalesSerializer)
from django.db.transaction import atomic
from django.utils.timezone import make_aware
from django_filters import CharFilter
from django_filters import rest_framework as django_filters
from rest_framework import exceptions, filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class SalesFilter(django_filters.FilterSet):
    Created_Time_Start = CharFilter(method='filter_Created_Time_Start')
    Created_Time_End = CharFilter(method='filter_Created_Time_End')
    
    class Meta:
        model = Sales
        fields = '__all__'

    def filter_Created_Time_Start(self, queryset, name, value):
        converted_date = make_aware(datetime.fromtimestamp(int(value)))
        return queryset.filter(Created_Time__gte=converted_date)

    def filter_Created_Time_End(self, queryset, name, value):
        converted_date = make_aware(datetime.fromtimestamp(int(value)))
        return queryset.filter(Created_Time__lte=converted_date)

class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all().order_by('Sales_ID')
    serializer_class = SalesSerializer
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SalesFilter

    @atomic
    @action(detail=False, methods=['post'], authentication_classes=[])
    def add(self, request):
        serializer = SalesAddSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @atomic
    @action(detail=False, methods=['get'], url_path='get/(?P<pk>\d+)')
    def get(self, request, pk):
        try:
            instance = Sales.objects.get(Sales_ID=pk, Author_ID=self.request.user.Author_ID)
        except Sales.DoesNotExist:
            raise exceptions.NotFound()
        serializer = SalesSerializer(instance=instance)
        return Response(serializer.data)

    @atomic
    @action(detail=False, methods=['get'])
    def get_my_sales(self, request): 
        queryset = self.filter_queryset(self.get_queryset()).filter(Author_ID=self.request.user.Author_ID)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data if serializer.data else 'List data empty.')
