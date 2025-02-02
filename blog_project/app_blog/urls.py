from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, LikeCreateView, check_authentication, \
    LikeListView

urlpatterns = [
    #Each line defines a path (URL) that is linked to a specific View for handling posts, comments and likes.
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('likes/', LikeListView.as_view(), name='like-list'),
    path('likes/create/', LikeCreateView.as_view(), name='like-create'),
    path('check-auth/', check_authentication, name='check-auth'),
]