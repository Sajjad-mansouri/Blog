from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=50,unique=True)
    avatar=models.ImageField(upload_to='media/avatar',blank=True,null=True)