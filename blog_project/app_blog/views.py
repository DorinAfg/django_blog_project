from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like
from .serializers import ProfileSerializer, PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Like, Post, Comment
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


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
class LikeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        post_id = data.get('post')
        comment_id = data.get('comment')

        # ודא לפחות אחד מהם נמסר (פוסט או תגובה)
        if not post_id and not comment_id:
            return Response({"detail": "Either 'post' or 'comment' is required"}, status=status.HTTP_400_BAD_REQUEST)

        # אם ה-user שולח גם פוסט וגם תגובה, יש להחזיר שגיאה
        if post_id and comment_id:
            return Response({"detail": "You cannot like both a post and a comment at the same time"}, status=status.HTTP_400_BAD_REQUEST)

        # אם נבחר פוסט, נוודא שהוא קיים
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

            # מניעת לייק כפול לפוסט
            if Like.objects.filter(user=request.user, post=post).exists():
                return Response({"detail": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

            # יצירת הלייק לפוסט
            like = Like.objects.create(user=request.user, post_id=post_id)

        # אם נבחרה תגובה, נוודא שהיא קיימת
        elif comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

            # מניעת לייק כפול לתגובה
            if Like.objects.filter(user=request.user, comment_id=comment_id).exists():
                return Response({"detail": "You already liked this comment"}, status=status.HTTP_400_BAD_REQUEST)

            # יצירת הלייק לתגובה
            like = Like.objects.create(user=request.user, comment_id=comment_id)

        return Response({"message": "Liked successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def check_authentication(request):
    if request.user.is_authenticated:
        return Response({"message": f"You are logged in as {request.user.username}"})
    return Response({"message": "You are not logged in"}, status=401)