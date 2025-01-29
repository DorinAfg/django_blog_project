from rest_framework import serializers
from .models import Profile, Post, Comment, Like
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']  # רשום את השדות שמוצגים לך
        read_only_fields = ['author', 'created_at']  # הערכים שמוזנים אוטומטית, לא ישלחו ב-POST

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # עדיין מוגדר כ-read_only

    class Meta:
        model = Like
        fields = ['id', 'user', 'post']  # רישום השדות הספציפיים שצריכים להיכלל ב-POST
        read_only_fields = ['user']  # קבעו ש-read_only יהיו רק שדות שצריך

