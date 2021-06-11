from django.urls import path

from .views import (ReviewListAPIView,
                    ReviewDetailAPIView,
                    CommentListAPIView,
                    CommentDetailAPIView)

app_name = 'reviews'

urlpatterns = [
    path('v1/titles/<int:title_id>/reviews/',
         ReviewListAPIView.as_view(), name='reviews_list'),
    path('v1/titles/<int:title_id>/reviews/<int:review_id>/',
         ReviewDetailAPIView.as_view(),
         name='reviews_detail'),

    path('v1/titles/<int:title_id>/reviews/<int:review_id>/comments/',
         CommentListAPIView.as_view(),
         name='comments_list'),

    path('v1/titles/<int:title_id>/'
         'reviews/<int:review_id>/'
         'comments/<int:comment_id>/',
         CommentDetailAPIView.as_view(), name='comments_detail'),
]
