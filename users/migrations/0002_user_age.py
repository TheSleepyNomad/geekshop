# Generated by Django 3.2.7 on 2021-09-29 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(default=18, verbose_name='Возраст'),
        ),
    ]
