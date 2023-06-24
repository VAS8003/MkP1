from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Good(models.Model):
    title = models.CharField(max_length=255, verbose_name="Найменування")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    annotation = models.TextField(max_length=500, verbose_name="Короткий опис")
    description = models.TextField(blank=True, verbose_name="Опис")
    photo = models.ImageField(blank=True, verbose_name="Фотографія")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Створив",
                              editable=False)
    provider = models.CharField(max_length=255, blank=True, verbose_name="Поставщик")
    full_stock = models.IntegerField(default=0, verbose_name="Стандарт наявності")
    article = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Артикул")
    price_opt = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Ціна ОПТ")
    price_b2c = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Ціна Роздріб")
    price_drop = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Ціна DROP")
    price_mrc = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="МРЦ")
    opt_stock = models.IntegerField(default=0, verbose_name="Опт наявність")
    b2c_stock = models.IntegerField(default=0, verbose_name="Роздріб наявність")
    drop_stock = models.IntegerField(default=0, verbose_name="DROP наявність")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категорія")
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, null=True, verbose_name="Бренд")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('good', kwargs={'good_slug': self.slug})

    class Meta:
        verbose_name = "Товари"
        verbose_name_plural = "Товари"
        ordering = ['-time_create', 'title']


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name="Бенд")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренди"
        verbose_name_plural = "Бренди"
        ordering = ['id', 'name']

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Категорії")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорії"
        verbose_name_plural = "Категорії"
        ordering = ['id', 'name']

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
