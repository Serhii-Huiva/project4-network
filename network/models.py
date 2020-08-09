from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.TextField()
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.time} : {self.user} say: {self.content}"

class Follow(models.Model):
    user = models.CharField(max_length=64)
    following = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user}, following {self.following}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    user = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user} liked {self.post}"
