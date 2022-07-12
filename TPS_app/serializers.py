from rest_framework import serializers
from TPS_app.models import Teams, Players, Locations, Schedules

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['idTeams','Teams_Name','Teams_Sponsor']

class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ['idPlayers','Players_Username','Players_Password','Players_Name',
                  'Players_Role','Players_ContactNo','idTeams']

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ['idLocations','Location_Name','Location_City','Location_Booking']

class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ['idSchedule','Teams1_ID','Teams2_ID','Match_date','idLocations','Result']