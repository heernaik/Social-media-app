# Generated by Django 3.2.9 on 2022-01-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_groupjointrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupjointrequest',
            name='is_accept',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupjointrequest',
            name='is_reject',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupjointrequest',
            name='next_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
