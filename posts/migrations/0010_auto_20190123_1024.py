# Generated by Django 2.1.4 on 2019-01-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20190123_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]