# Generated by Django 4.0 on 2023-02-09 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='sender',
        ),
    ]