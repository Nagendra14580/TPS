import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework import exceptions

from TPS_app.models import Teams, TPS_Users, Locations, Schedules

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['teams_name','teams_sponsor','team_capitan','teams_players','is_approved']

class TPSUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPS_Users
        fields = ['email','password','name','email','contactNo','teams_name',
                  'is_capitan','is_active']

class TPSUserRegistrationRequsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPS_Users
        fields = ('email','password','is_capitan','teams_name')

    def create(self, validated_data):
        auth_user = TPS_Users.objects.create_user(**validated_data)
        return auth_user
        
class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ['idLocations','location_name','location_city','isBooked','booking_date']

class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ['idSchedule','Teams1_ID','Teams2_ID','Match_date','idLocations','Result']

