# Generated by Django 4.0.2 on 2023-01-24 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_product_lan_product_lan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='lan',
            new_name='language',
        ),
    ]
