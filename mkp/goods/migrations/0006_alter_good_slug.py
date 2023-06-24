# Generated by Django 4.2.1 on 2023-06-21 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_alter_good_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
