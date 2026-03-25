from rest_framework import serializers
from .models import Keyword, ContentItem, Flag


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['id', 'title', 'source', 'body', 'last_updated']


class FlagSerializer(serializers.ModelSerializer):
    keyword = KeywordSerializer(read_only=True)
    content_item = ContentItemSerializer(read_only=True)

    class Meta:
        model = Flag
        fields = ['id', 'keyword', 'content_item', 'score', 'status']


class FlagStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ['status']