from .models import User, ContentItem
from rest_framework import serializers


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContentItem
        fields= '__all__'

class UserSerializer(serializers.ModelSerializer):
    contentItem = ContentItemSerializer(read_only=True, many=True)
    class Meta:
        model= User
        fields='__all__'