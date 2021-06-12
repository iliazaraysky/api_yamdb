from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.permissions import IsAuthor
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer


class ReviewListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor)
    serializer_class = ReviewSerializer

    def get_object(self):
        obj = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        self.check_object_permissions(self.request, obj)
        return obj


class CommentListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor)
    serializer_class = CommentSerializer

    def get_object(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        comment_id = self.kwargs.get('comment_id')
        obj = get_object_or_404(
            Comment,
            review__title_id=title_id,
            review_id=review_id,
            id=comment_id
        )

        self.check_object_permissions(self.request, obj)
        return obj
