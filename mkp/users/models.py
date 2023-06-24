from django.db import models
from django.contrib.auth.models import AbstractUser

# from baskets.models import Cart


class User(AbstractUser):
    user_image = models.ImageField(upload_to='uses_images', blank=True, verbose_name='Фото користувача')
    seller_image = models.ImageField(upload_to='uses_images', blank=True, verbose_name='Фото продавця')
    seller_name = models.CharField(max_length=50, blank=True, verbose_name='Назва продавця')
    seller_status = models.BooleanField(default=False, verbose_name='Статус продавця')
    drop_status = models.BooleanField(default=False, verbose_name='Статус DROP')
    provider_status = models.BooleanField(default=False, verbose_name='Статус PROVIDER')



