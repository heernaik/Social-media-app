# Generated by Django 3.2.9 on 2022-01-21 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_tumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tumbnail',
            new_name='thumbnail',
        ),
    ]
