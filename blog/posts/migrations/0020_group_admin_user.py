# Generated by Django 3.2.9 on 2022-01-29 17:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0019_restrictusercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='admin_user',
            field=models.ManyToManyField(related_name='admin_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
