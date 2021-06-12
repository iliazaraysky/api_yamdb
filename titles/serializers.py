from rest_framework import serializers
from .models import Title, Category, Genre
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class RepresentCategory(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = CategorySerializer(obj)
        return serializer.data


class RepresentGenre(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = GenreSerializer(obj)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = RepresentCategory(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = RepresentGenre(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
