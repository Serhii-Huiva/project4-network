# Generated by Django 3.0.8 on 2020-08-04 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
