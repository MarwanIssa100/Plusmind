from rest_framework import serializers
from .models import Post, Category, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['creator', 'category', 'title', 'slug', 'excerpt', 'content', 'published', 'status', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        models = Comment
        fields = ['post', 'user', 'comment', 'created_at', 'updated_at']
