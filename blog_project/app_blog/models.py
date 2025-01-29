from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#A model representing a user profile.
class Profile(models.Model):
    #"One-to-one" relationship per user (each user has only one profile).
    #on_delete=models.CASCADE - If the user is deleted, the profile will also be deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    #User image field. The images will be saved in the 'avatars/' folder.
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    #Function to display the profile as text (returns the username).
    def __str__(self):
        return self.user.username



#A model representing a blog post.
class Post(models.Model):
    #"One-to-many" relationship to a user (a user can write multiple posts).
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

#A model representing a blog comment.
class Comment(models.Model):
    #A "one-to-many" relationship to a post (a post can have multiple comments).
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    #"One-to-many" relationship to a user (a user can write multiple comments).
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #Recursive relationship to another response (a response can be a response to another response).
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    #Displays the name of the comment plus its post name.
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"



##A model representing a blog Like.
class Like(models.Model):
    #"One-to-many" relationship to the user (user can give likes).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    #Optional link to the post (like the post).
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    #Optional link to comment (like comment).
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    #Displays text describing the like:
    created_at = models.DateTimeField(default=timezone.now)  # פתרון שיקבע תאריך לכל הרשומות הישנות
    def __str__(self):
        if self.post:
            #If it's a like for a post, indicates the name of the post.
            return f"Like by {self.user} on post {self.post.title}"
        #If this is a like for a comment, specifies the comment ID.
        return f"Like by {self.user} on comment {self.comment.id}"