from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    location_root_name = serializers.CharField(source='location_root.name', read_only=True)
    rack_number = serializers.CharField(source='rack.number', read_only=True)
    section_number = serializers.CharField(source='section.number', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'year', 'genre', 'isbn', 'pages',
            'description', 'cover', 'total_copies', 'available_copies',
            'location_root', 'rack', 'section',
            'location_root_name', 'rack_number', 'section_number',
        ]