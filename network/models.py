from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.TextField()
    time = models.DateTimeField()
    like = models.IntegerField()

    def __str__(self):
        return f"{self.time} : {self.user} say: {self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "content": self.content,
            "datetime": self.time.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like
        }

class Follow(models.Model):
    user = models.CharField(max_length=64)
    following = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user}, following {self.following}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "following": self.following
        }

    
