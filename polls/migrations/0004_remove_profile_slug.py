# Generated by Django 4.0 on 2022-04-02 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_profile_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
    ]