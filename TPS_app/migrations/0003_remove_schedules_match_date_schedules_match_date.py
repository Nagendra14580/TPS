# Generated by Django 4.0.6 on 2022-07-11 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TPS_app', '0002_alter_schedules_match_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedules',
            name='match_date',
        ),
        migrations.AddField(
            model_name='schedules',
            name='Match_date',
            field=models.TextField(default='', max_length=20),
        ),
    ]
