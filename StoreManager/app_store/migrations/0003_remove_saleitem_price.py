# Generated by Django 4.0 on 2024-02-27 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0002_remove_sale_goods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleitem',
            name='price',
        ),
    ]