# Generated by Django 5.0 on 2023-12-27 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_item_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
