# Generated by Django 4.0 on 2024-02-14 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provider',
            options={'verbose_name': 'поставщик', 'verbose_name_plural': 'поставщики'},
        ),
        migrations.AlterModelTable(
            name='provider',
            table='providers',
        ),
    ]
