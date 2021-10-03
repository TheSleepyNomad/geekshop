from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save

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


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOICES = ((MALE, 'M'), (FEMALE, 'W'))

    user = models.OneToOneField(
        User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='тэг', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', blank=True)
    gender = models.CharField(
        verbose_name='пол', choices=GENDER_CHOICES, blank=True, default=None, max_length=2, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
