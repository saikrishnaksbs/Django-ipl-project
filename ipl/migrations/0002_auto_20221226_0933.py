# Generated by Django 2.2 on 2022-12-26 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipl', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveries',
            old_name='batting_team',
            new_name='battingteam',
        ),
    ]
