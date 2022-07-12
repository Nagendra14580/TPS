# Generated by Django 4.0.6 on 2022-07-11 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('idLocations', models.AutoField(primary_key=True, serialize=False)),
                ('Location_Name', models.CharField(max_length=50)),
                ('Location_City', models.CharField(max_length=20)),
                ('Location_Booking', models.IntegerField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('idTeams', models.AutoField(primary_key=True, serialize=False)),
                ('Teams_Name', models.CharField(max_length=50)),
                ('Teams_Sponsor', models.CharField(max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Teams',
            },
        ),
        migrations.CreateModel(
            name='Schedules',
            fields=[
                ('idSchedule', models.AutoField(primary_key=True, serialize=False)),
                ('match_date', models.DateTimeField(auto_now_add=True)),
                ('Result', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('Teams1_ID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Teams1_ID', to='TPS_app.teams')),
                ('Teams2_ID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Teams2_ID', to='TPS_app.teams')),
                ('idLocations', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TPS_app.locations')),
            ],
            options={
                'db_table': 'Schedules',
            },
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('idPlayers', models.AutoField(primary_key=True, serialize=False)),
                ('Players_Username', models.CharField(max_length=20)),
                ('Players_Password', models.CharField(max_length=20)),
                ('Players_Name', models.CharField(max_length=50)),
                ('Players_Role', models.IntegerField(default=0)),
                ('Players_ContactNo', models.CharField(max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('idTeams', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TPS_app.teams')),
            ],
            options={
                'db_table': 'Players',
            },
        ),
    ]