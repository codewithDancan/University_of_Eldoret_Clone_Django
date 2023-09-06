from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your models here.
User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    email = models.EmailField(unique=True)
    forget_password_token = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_img = models.ImageField(
        upload_to='profile_images', default='blank_profile.jpg')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
