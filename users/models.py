from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta


# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True)
    age = models.PositiveIntegerField(default=18, verbose_name="Возраст")
    language = models.CharField(
        max_length=3, verbose_name='язык пользователя', default='ENG')

    activation_key = models.CharField(max_length=128, blank=True,)
    # activation_key_expires = models.DateTimeField(default=(now()+timedelta(hours=48)))
    activation_key_expires = models.DateTimeField(
        auto_now_add=True, blank=True)

    def is_activation_key_expired(self):
        if now() < self.activation_key_expires + timedelta(hours=48):
            return False
        return True
