from bookstore.app.models import Book, Sales
from rest_framework import serializers


class SalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sales
        fields = '__all__'


class SalesAddSerializer(serializers.ModelSerializer):
    Name = serializers.CharField()
    Email = serializers.EmailField()
    Quantity = serializers.IntegerField(min_value=1)
    Book_ID = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Sales
        fields = ['Name', 'Email', 'Quantity', 'Book_ID']

    def create(self, validated_data):
        book = validated_data.pop('Book_ID')
        validated_data['Recepient_Name'] = validated_data.pop('Name')
        validated_data['Recepient_Email'] = validated_data.pop('Email')
        validated_data['Book_Title'] = book.Title
        validated_data['Author_ID'] = book.Author_ID
        validated_data['Price_Per_Unit'] = book.Price
        validated_data['Price_Total'] = book.Price * validated_data['Quantity']
        return super().create(validated_data)
