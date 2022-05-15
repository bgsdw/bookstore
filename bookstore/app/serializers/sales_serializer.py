from bookstore.app.models import Sales
from rest_framework import serializers


class SalesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sales
        fields = '__all__'
