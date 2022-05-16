from bookstore.app.models import Book, Sales
from rest_framework import serializers


class SalesSerializer(serializers.ModelSerializer):
    Created_Time = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = '__all__'

    def get_Created_Time(self, obj):
        return int(obj.Created_Time.replace(microsecond=0).timestamp())


class SalesAddSerializer(serializers.ModelSerializer):
    Name = serializers.CharField()
    Email = serializers.EmailField()
    Quantity = serializers.IntegerField(min_value=1)
    Book_ID = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Sales
        fields = ['Name', 'Email', 'Quantity', 'Book_ID']

    def create(self, validated_data):
        # prepare the sales data
        book = validated_data.pop('Book_ID')
        validated_data['Recepient_Name'] = validated_data.pop('Name')
        validated_data['Recepient_Email'] = validated_data.pop('Email')
        validated_data['Book_Title'] = book.Title
        validated_data['Author_ID'] = book.Author_ID
        validated_data['Price_Per_Unit'] = book.Price
        validated_data['Price_Total'] = book.Price * validated_data['Quantity']

        # check the book stock
        if book.Stock == 0:
            raise serializers.ValidationError({'detail': f'Book stock is empty.'})
        elif validated_data['Quantity'] > book.Stock:
            raise serializers.ValidationError({'detail': f'Book stock is only {book.Stock} left.'})

        # update book stock
        book.Stock = book.Stock - validated_data['Quantity']
        book.save()
        return super().create(validated_data)
