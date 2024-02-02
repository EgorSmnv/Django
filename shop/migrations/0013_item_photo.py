# Generated by Django 5.0 on 2024-01-18 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_uploadfiles_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
