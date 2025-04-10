# Generated by Django 5.1 on 2025-02-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0002_alter_movieprogress_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieprogress',
            name='total_seconds',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='movieprogress',
            name='watched_seconds',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='tvprogress',
            name='total_seconds',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='tvprogress',
            name='watched_seconds',
            field=models.FloatField(default=0),
        ),
    ]
