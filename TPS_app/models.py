from django.db import models
from datetime import datetime

# Create yo9ur models here.
class Teams(models.Model):
    idTeams = models.AutoField(primary_key=True)
    Teams_Name = models.CharField(max_length = 50)
    Teams_Sponsor = models.CharField(max_length = 20)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Teams_Name

    class Meta:
        db_table = 'Teams'

class Players(models.Model):
    idPlayers = models.AutoField(primary_key=True)
    Players_Username = models.CharField(max_length = 20)
    Players_Password = models.CharField(max_length = 20)
    Players_Name = models.CharField(max_length = 50)
    Players_Role = models.IntegerField(default=0)
    Players_ContactNo = models.CharField(max_length = 20)
    idTeams = models.ForeignKey(Teams, default = 1, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Players_Username

    class Meta:
        db_table = 'Players'

class Locations(models.Model):
    idLocations = models.AutoField(primary_key=True)
    Location_Name = models.CharField(max_length = 50)
    Location_City = models.CharField(max_length = 20)
    Location_Booking = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Location_Name

    class Meta:
        db_table = 'Locations'

class Schedules(models.Model):
    idSchedule = models.AutoField(primary_key=True)
    Teams1_ID = models.ForeignKey(Teams, default = 1, on_delete=models.CASCADE, related_name='Teams1_ID')
    Teams2_ID = models.ForeignKey(Teams, default = 1, on_delete=models.CASCADE, related_name='Teams2_ID')
    Match_date = models.TextField(max_length = 20, default='')
    idLocations = models.ForeignKey(Locations, default = 1, on_delete=models.CASCADE)
    Result = models.IntegerField(default = 0)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.idSchedule

    class Meta:
        db_table = 'Schedules'