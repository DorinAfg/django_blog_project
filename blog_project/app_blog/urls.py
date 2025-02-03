from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, LikeCreateView, check_authentication, \
    LikeListView, get_post_likes_count

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('likes/', LikeListView.as_view(), name='like-list'),
    path('likes/create/', LikeCreateView.as_view(), name='like-create'),
    path('check-auth/', check_authentication, name='check-auth'),
    path('posts/<int:post_id>/likes_count/', get_post_likes_count, name='post-likes-count'),
]