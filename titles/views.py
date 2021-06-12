from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets, filters
from titles.models import Category, Title, Genre
from rest_framework.permissions import IsAdminUser
from .filters import FilterForTitle
from .permissions import IsAdminOrReadOnly
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer)


class APICategory(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class APICategoryDetail(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class APIGenres(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class APIGenresDelete(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class APITitles(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle

    class Meta:
        ordering = ('id',)
