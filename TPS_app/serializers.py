from rest_framework import serializers
from rest_framework.authtoken.models import Token
from TPS_app.models import Teams, TPS_Users, Locations, Schedules
from rest_framework_simplejwt.tokens import RefreshToken

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['idTeams','teams_name','teams_sponsor','teams_players','is_approved']

class TPSUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPS_Users
        fields = ['idPlayers','email','password','name','email','ContactNo','idTeams',
                  'is_capitan','is_active']

class TPSUserRegistrationRequsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPS_Users
        fields = ('email','password')

    def create(self, validated_data):
        auth_user = TPS_Users.objects.create_user(**validated_data)
        return auth_user
        
class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ['idLocations','location_name','location_city','isBooked']

class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ['idSchedule','Teams1_ID','Teams2_ID','Match_date','idLocations','Result']

