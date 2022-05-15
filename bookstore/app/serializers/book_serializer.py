from django.utils import timezone
from bookstore.app.models import Author, Book
from rest_framework import serializers

from bookstore.app.services.file_service import FileService


class BookSerializer(serializers.ModelSerializer):
    Author_ID = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), required=False)
    Cover_URL = serializers.CharField(required=False)
    Cover_Image_Base64 = serializers.CharField(write_only=True)
    Image_Extension = serializers.CharField(write_only=True)
    Author_Pen_Name = serializers.CharField(source='Author_ID.Pen_Name', read_only=True)

    class Meta:
        model = Book
        exclude = ['Created_Time']

    def create(self, validated_data):
        validated_data['Author_ID'] = self.context['request'].user
        image_base64 = validated_data.pop('Cover_Image_Base64')
        image_ext = validated_data.pop('Image_Extension')
        if image_ext not in ('jpg', 'png', 'jpeg'):
            raise serializers.ValidationError({'detail': 'Image_Extension should be in jpg, png or jpeg.'})
        validated_data['Cover_URL'] = FileService.base64_to_file(image_base64, f'{validated_data["Title"]}-{timezone.now().timestamp()}.{image_ext}')
        return super().create(validated_data)

class BookUpdateSerializer(BookSerializer):
    Cover_Image_Base64 = None
    Image_Extension = None

class BookCoverUpdateSerializer(BookSerializer):

    class Meta:
        model = Book
        fields = ['Cover_Image_Base64', 'Image_Extension']

    def update(self, instance, validated_data):
        image_base64 = validated_data.pop('Cover_Image_Base64')
        image_ext = validated_data.pop('Image_Extension')
        if image_ext not in ('jpg', 'png', 'jpeg'):
            raise serializers.ValidationError({'detail': 'Image_Extension should be in jpg, png or jpeg.'})
        validated_data['Cover_URL'] = FileService.base64_to_file(image_base64, f'{instance.Title}-{timezone.now().timestamp()}.{image_ext}')
        return super().update(instance, validated_data)
