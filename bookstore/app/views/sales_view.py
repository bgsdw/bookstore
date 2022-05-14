from bookstore.app.models import Sales
from bookstore.app.serializers.sales_serializer import SalesSerializer
from rest_framework import viewsets


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
