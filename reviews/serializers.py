from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from titles.models import Title
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        title_id = self.context['view'].kwargs.get('title_id')
        attrs['title'] = get_object_or_404(
            Title,
            id=title_id
        )
        if not self.partial and Review.objects.filter(
                title=attrs['title'],
                author=self.context['request'].user).exists():
            raise ValidationError(
                {'author': 'Вы уже оставляли отзыв на это произведение'})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    def validate(self, attrs):
        review_id = self.context['view'].kwargs.get('review_id')
        title_id = self.context['view'].kwargs.get('title_id')
        attrs['review'] = get_object_or_404(
            Review,
            id=review_id,
            title_id=title_id
        )
        return attrs
