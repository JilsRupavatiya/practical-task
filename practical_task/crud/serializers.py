from rest_framework import serializers
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", 'title', 'content']
        read_only_fields = ['id', 'created_by']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['created_by'] = user
        
        return super().create(validated_data)
