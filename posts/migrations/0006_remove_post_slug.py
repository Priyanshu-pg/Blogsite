# Generated by Django 2.1.4 on 2019-01-15 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20190115_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
