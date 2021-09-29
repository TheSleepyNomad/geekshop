from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True)
    age = models.PositiveIntegerField(default=18, verbose_name="Возраст")
    language = models.CharField(max_length=3,verbose_name='язык пользователя',default='ENG')
