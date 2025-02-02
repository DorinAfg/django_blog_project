from rest_framework import serializers
from .models import Profile, Post, Comment, Like

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        #Means to automatically insert all Profile fields into JSON.
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post']
        read_only_fields = ['user']

