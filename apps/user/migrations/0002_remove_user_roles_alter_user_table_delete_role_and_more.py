# Generated by Django 5.0 on 2023-12-23 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
