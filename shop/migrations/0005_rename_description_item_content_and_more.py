# Generated by Django 5.0 on 2023-12-27 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_item_in_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='description',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='title',
        ),
    ]