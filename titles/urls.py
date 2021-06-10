from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from titles import views

router = DefaultRouter()
router.register('v1/titles', views.APITitles, basename='api_title')

app_name = 'titles'

urlpatterns = [
    path('', include(router.urls)),
    path('v1/categories/', views.APICategory.as_view(),
         name='api_category'),
    path('v1/genres/', views.APIGenres.as_view(), name='api_genre'),
    path('v1/genres/<slug>/', views.APIGenresDelete.as_view(),
         name='api_genre_delete'),
    path('v1/categories/<slug>/', views.APICategoryDetail.as_view(),
         name='api_category_detail'),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh')
]
