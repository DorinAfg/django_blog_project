
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Like, Post, Comment
from .serializers import LikeSerializer
from rest_framework.exceptions import ValidationError



#class that represents the view that handles managing posts
#return a list of the posts and creating posts
#generics.ListCreateAPIView is a ready class in DRF, handle GET and POST
class PostListCreateView(generics.ListCreateAPIView):
    #queryset: Defines the objects that will be returned by the API when making a call.
    #Post.objects.all() means that a list of posts (objects from the Post model) will be given all posts from the database.
    queryset = Post.objects.all()
    #serializer_class: Defines the serializer that be used to convert the information between the posts (Post objects)
    #PostSerializer- serializer responsible for converting the Post model to the format received in the API.
    serializer_class = PostSerializer
    #permission_classes: Defines the permissions assigned to this view.
    #IsAuthenticatedOrReadOnly: access permission allows unlogged users to only read the data (READ)
    #only login users to perform write operations (CREATE, UPDATE, DELETE).
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #An action performed after a POST call fails the serializer, after creating a new object לחזור על זה
    def perform_create(self, serializer):
        #when user creates a new post, the author field will be automatically field with the login user.
        #author=self.request.user - the same user who is making the request
        serializer.save(author=self.request.user)



#class that represents the view that handles managing post (a single post)
#displaying and editing a single post
#generics.RetrieveUpdateDestroyAPIView is a ready class in DRF, handle GET\ PUSH\ PATCH\ DELETE
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



#class that handles displaying a list and creating comments to posts
#generics.ListCreateAPIView is a ready class in DRF, handle GET and POST
class CommentListCreateView(generics.ListCreateAPIView):
    #Comment.objects.all() means that a list of Comment (objects from the Comment model) will be given all posts from the database.
    queryset = Comment.objects.all()
    #CommentSerializer- serializer responsible for convert the response information into a JSON format (suitable for the API)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


#class that creates the view for creating a like for a post or comment.
#APIView is a base class that allows for handling API operations in general, handle POST
class LikeCreateView(generics.CreateAPIView):  # שימוש ב-CreateAPIView במקום APIView
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        comment_id = self.request.data.get('comment')

        if not post_id and not comment_id:
            raise ValidationError({"detail": "Either 'post' or 'comment' is required"})

        if post_id and comment_id:
            raise ValidationError({"detail": "You cannot like both a post and a comment at the same time"})

        if post_id and Like.objects.filter(user=self.request.user, post_id=post_id).exists():
            raise ValidationError({"detail": "You already liked this post"})

        if comment_id and Like.objects.filter(user=self.request.user, comment_id=comment_id).exists():
            raise ValidationError({"detail": "You already liked this comment"})

        serializer.save(user=self.request.user, post_id=post_id if post_id else None,
                        comment_id=comment_id if comment_id else None)


class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.request.query_params.get('post', None)
        comment_id = self.request.query_params.get('comment', None)

        if post_id:
            return Like.objects.filter(post_id=post_id)
        elif comment_id:
            return Like.objects.filter(comment_id=comment_id)
        else:
            return Like.objects.all()

@api_view(['GET'])
def check_authentication(request):
    if request.user.is_authenticated:
        return Response({"message": f"You are logged in as {request.user.username}"})
    return Response({"message": "You are not logged in"}, status=401)

