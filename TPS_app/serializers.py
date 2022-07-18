import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework import exceptions

from TPS_app.models import Teams, TPS_Users, Locations, Schedules

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['idTeams','teams_name','teams_sponsor','teams_players','is_approved']

class TPSUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPS_Users
        fields = ['idPlayers','email','password','name','email','contactNo','idTeams',
                  'is_capitan','is_active']

class TPSUserRegistrationRequsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPS_Users
        fields = ('email','password')

    def validate_password(self, data):
        # validators.validate_password(password=data, user=User)
        # return data
        
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = TPSUserRegistrationRequsetSerializer(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(TPSUserRegistrationRequsetSerializer, self).validate(data)

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

