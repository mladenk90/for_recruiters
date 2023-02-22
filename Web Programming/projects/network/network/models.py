from django.contrib.auth.models import AbstractUser
from django.db import models

# class for user info
class User(AbstractUser):
    pass
# class for post info
class Post(models.Model):
    content = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} posted by {self.owner} at {self.date.strftime('%d %b %Y %H:%M:%S')}"
# class for following info
class Following(models.Model):
    owner_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    owner_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")

    def __str__(self):
        return f"{self.owner_following} is following {self.owner_follower}"
# class for like info
class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"{self.owner} like {self.post}"