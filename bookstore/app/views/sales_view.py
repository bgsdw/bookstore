from bookstore.app.models import Sales
from bookstore.app.serializers.sales_serializer import SalesAddSerializer, SalesSerializer
from django.db.transaction import atomic
from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer

    @atomic
    @action(detail=False, methods=['post'])
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
            return self.get_paginated_response({'List_Data': serializer.data})
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({'List_Data': serializer.data})
