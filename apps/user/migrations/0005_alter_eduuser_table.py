# Generated by Django 5.0 on 2023-12-24 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_eduuser_delete_user'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='eduuser',
            table='edu_user',
        ),
    ]