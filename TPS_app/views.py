import requests
import string, random

from django.db.models import Q
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_condition import Or,  And

from TPS_app.models import Teams, TPS_Users, Locations, Schedules
from TPS_app.serializers import TeamsSerializer, TPSUserRegistrationRequsetSerializer
from TPS_app.serializers import LocationsSerializer, SchedulesSerializer
from TPS_app.serializers import TPSUserResponseSerializer
from TPS_app.custom_permissions import IsAdmin, IsCapitan
from TPS_app.common import Common

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status= status.HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status= status.HTTP_404_NOT_FOUND)
    elif 'Terras_' in password:
        return Response({'token': token.key,
                        'Message': 'Change the password'},
                         status= status.HTTP_200_OK)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status= status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([And(IsAuthenticated, IsAdmin)])
def create_user(request):
    validated_data = {}
    validated_data['email'] = request.data['email']
    validated_data['password'] = Common.generate_random_password()
    print(validated_data)
    tps_reg_ser = TPSUserRegistrationRequsetSerializer(data = validated_data)
    valid = tps_reg_ser.is_valid(raise_exception=True)

    if valid:
        tps_reg_ser.save()
        status_code = status.HTTP_201_CREATED
        response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'data': tps_reg_ser.data
            }
        return Response(response, status=status_code)   
    return Response(tps_reg_ser.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        player = TPS_Users.objects.get(idPlayers = request.data['idPlayers'])
    except TPS_Users.DoesNotExist:
        return Response({'msg':'No Players Found', 'staus':status.HTTP_404_NOT_FOUND})
    serializers = TPSUserResponseSerializer(player, request.data, partial=True)
    if serializers.is_valid():
        print(serializers)
        serializers.save()
        status_code = status.HTTP_200_OK
        response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Password Changed Successfully!',
                'data': serializers.data
            }
        return Response(response, status = status_code)

@csrf_exempt
@api_view(['GET', 'POST','PUT','PATCH','DELETE'])
@permission_classes(And(IsAuthenticated, Or(IsAdmin, IsCapitan)))
def teams_view(request):
    if request.method == 'GET':
        if 'idTeams' in request.data.keys():
            try:
                team = Teams.objects.get(idTeams = request.data['idTeams'])
                serializers = TeamsSerializer(team)
                response = Common.return_response(True, status.HTTP_200_OK, 
                                                 'Teams Data', serializers.data)
                return Response(response, status = status.HTTP_200_OK)
            except Teams.DoesNotExist:
                response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                                 'No Teams Found')
                return Response(response, status = status.HTTP_404_NOT_FOUND)
        else:
            teams = Teams.objects.all()
            serializers = TeamsSerializer(teams, many=True)
            response = Common.return_response(True, status.HTTP_200_OK, 
                                                 'Teams Data', serializers.data)
            return Response(response, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        data['teams_players'] = request.user.idPlayers
        serializers = TeamsSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            response = Common.return_response(True, status.HTTP_201_CREATED, 
                                                 'Teams Data created', serializers.data)
            return Response(response, status = status.HTTP_201_CREATED)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        print(request.data)
        try:
            team = Teams.objects.get(idTeams = request.data['idTeams'])
        except Teams.DoesNotExist:
            response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                              'pass idTeams', '')
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        serializers = TeamsSerializer(team, request.data)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            response = Common.return_response(True, status.HTTP_200_OK, 
                                             'Teams Data Updated', serializers.data)
            return Response(response,  status = status.HTTP_200_OK)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        print(request.data)
        try:
            team = Teams.objects.get(idTeams = request.data['idTeams'])
        except Teams.DoesNotExist:
            response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                              'pass idTeams', '')
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        serializers = TeamsSerializer(team, request.data, partial=True)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            response = Common.return_response(True, status.HTTP_200_OK, 
                                             'Teams Data Updated', serializers.data)
            return Response(response,  status = status.HTTP_200_OK)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if 'idTeams' in request.data.keys():
            Teams.objects.filter(idTeams = request.data['idTeams']).delete()
            response = Common.return_response(True, status.HTTP_204_NO_CONTENT, 
                                             'Teams Data Deleted', '')
            return Response(response, status=status.HTTP_204_NO_CONTENT)
       
        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'POST','PUT','PATCH','DELETE'])
@permission_classes(And(IsAuthenticated, IsAdmin))
def locations_view(request):
    if request.method == 'GET':
        if 'idLocations' in request.data.keys():
            try:
                location = Locations.objects.get(idLocations = request.data['idLocations'])
                serializers = LocationsSerializer(location)
                return Response(serializers.data, status = status.HTTP_200_OK)
            except Locations.DoesNotExist:
                return Response({'msg':'No Locations Found', 'staus':status.HTTP_404_NOT_FOUND})
        else:
            locations = Locations.objects.all()
            serializers = LocationsSerializer(locations, many=True)
            return Response(serializers.data)
    elif request.method == 'POST':
        serializers = LocationsSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            response = Common.return_response(True, status.HTTP_201_CREATED, 
                                             'Locations Data Created', serializers.data)
            return Response(response, status=status.HTTP_201_CREATED)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        print(request.data)
        try:
            location = Locations.objects.get(idLocations = request.data['idLocations'])
        except Locations.DoesNotExist:
            response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                                 serializers.errors, '')
            return Response(response, status.HTTP_404_NOT_FOUND)
        serializers = LocationsSerializer(location, request.data, partial=True)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            response = Common.return_response(True, status.HTTP_200_OK, 
                                             'Locations Data Updated', serializers.data)
            return Response(response, status=status.HTTP_200_OK)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')   
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        print(request.data)
        try:
            location = Locations.objects.get(idLocations = request.data['idLocations'])
        except Locations.DoesNotExist:
            return Response({'msg':'No Locations Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = LocationsSerializer(location, request.data)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            response = Common.return_response(True, status.HTTP_200_OK, 
                                             'Locations Data Updated', serializers.data)
            return Response(response, status=status.HTTP_200_OK)
        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')   
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if 'idLocations' in request.data.keys():
            Locations.objects.filter(idLocations = request.data['idLocations']).delete()
            response = Common.return_response(True, status.HTTP_204_NO_CONTENT, 
                                             'Locations Data Deleted', '')
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes(And(IsAuthenticated, IsAdmin))
def schedules_view(request):
    if request.method == 'GET':
        if 'idSchedule' in request.data.keys():
            try:
                schedule = Schedules.objects.get(idSchedule = request.data['idSchedule'])
                serializers = SchedulesSerializer(schedule)
                return Response(serializers.data, status = status.HTTP_200_OK)
            except Schedules.DoesNotExist:
                return Response({'msg':'No Locations Found', 'staus':status.HTTP_404_NOT_FOUND})
        else:
            schedules = Schedules.objects.all()
            serializers = SchedulesSerializer(schedules, many=True)
            return Response(serializers.data)
    elif request.method == 'POST':
        serializers = SchedulesSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            location = Locations.objects.get(idSchedule = request.data['idLocations'])
            location.location_booking = True
            serializers = LocationsSerializer(location)
            if serializers.is_valid():
                serializers.save()

            response = Common.return_response(True, status.HTTP_201_CREATED, 
                                             'Schedule Created', serializers.data)
            return Response(response, status=status.HTTP_201_CREATED)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        print(request.data)
        try:
            schedule = Schedules.objects.get(idSchedule = request.data['idSchedule'])
        except Schedules.DoesNotExist:
            return Response({'msg':'No Schedules Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = SchedulesSerializer(schedule, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            response = Common.return_response(True, status.HTTP_200_OK, 
                                             'Schedules Data Updated', serializers.data)
            return Response(response,  status = status.HTTP_200_OK)
            
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        print(request.data)
        try:
            schedule = Schedules.objects.get(idSchedule = request.data['idSchedule'])
        except Schedules.DoesNotExist:
            return Response({'msg':'No Schedules Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = SchedulesSerializer(schedule, request.data)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            return Response(serializers.data,  status = status.HTTP_200_OK)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, serializers.errors, '')
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if 'idSchedule' in request.data.keys():
            Schedules.objects.filter(idSchedule = request.data['idSchedule']).delete()
            response = Common.return_response(True, status.HTTP_204_NO_CONTENT, 
                                             'schedules Data Deleted', '')
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = Common.return_response(False, status.HTTP_400_BAD_REQUEST, 
                                                 serializers.errors, '')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_schedules(request):
    if 'idPlayers' in request.data.keys():
        print(request.data) 
        try:
            player = TPS_Users.objects.get(idPlayers = request.data['idPlayers'])
            print(type(player))
            serializers = TPSUserResponseSerializer(player)
            print("players", serializers.data['idTeams'])
            schedules = Schedules.objects.filter(
                Q(teams1_ID=serializers.data['idTeams']) | Q(teams2_ID=serializers.data['idTeams'])).values(
                    'idSchedule','teams1_ID','teams2_ID','match_date','idLocations'
                )
            if len(schedules.values()) > 0:
                response = Common.return_response(True, status.HTTP_200_OK, 
                                                 'Schedules Details Fetched', schedules.values())
                return Response(response, status = status.HTTP_200_OK) 
            else:
                response = Common.return_response(True, status.HTTP_404_NOT_FOUND, 
                                                 'No Schedules Found')
                return Response(response, status = status.HTTP_404_NOT_FOUND)
        except TPS_Users.DoesNotExist:
            response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                                 'No Player Found')
            return Response(response, status = status.HTTP_404_NOT_FOUND)  
    else:
        response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                                 'Specify Players ID')
        return Response(response, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_team_members(request):
    if 'idPlayers' in request.data.keys(): 
        try:
            player = TPS_Users.objects.get(idPlayers = request.data['idPlayers'])
            serializers = TPSUserResponseSerializer(player)
            team_players = TPS_Users.objects.filter(idTeams=serializers.data['idTeams']).values('idPlayers','Players_Name')
            if len(team_players.values()) > 0:
                response = Common.return_response(True, status.HTTP_200_OK, 
                                                 'Team Details Fetched', team_players.values())
                return Response(response, status = status.HTTP_200_OK) 
            else:
                response = Common.return_response(True, status.HTTP_404_NOT_FOUND, 
                                                 'No Teams Found')
                return Response(response, status = status.HTTP_404_NOT_FOUND)
            
        except TPS_Users.DoesNotExist:
            response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                                 'No Player Found')
            return Response(response, status = status.HTTP_404_NOT_FOUND)  
    else:
        response = Common.return_response(False, status.HTTP_404_NOT_FOUND, 
                                                 'Specify Players ID')
        return Response(response, status = status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes(And(IsAuthenticated, IsCapitan))
def add_team_players(request):
    captain_id  = request.data['idPlayers']
    team_members = request.data['team_members']
    team_id = Common.get_team_id(captain_id)
    print("the teams_id", team_id)
    for member in team_members:
        team_count = TPS_Users.objects.filter(idTeams = team_id).count()
        team = Teams.object.get(idTeams = team_id)
        print("the team count is ",team_count)
        if team_count < 15 :
            player = TPS_Users.objects.get(idPlayers = member)
            player.idTeams = team_id
            team.teams_players = team.teams_players + ","+ member
            team_serializers = TeamsSerializer(team)
            tps_serializers = TPSUserResponseSerializer(player)
            if tps_serializers.is_valid():
                serializers.save()
                team_serializers.save()
                team_count = TPS_Users.objects.filter(idTeams = team_id).count()
        else:
            response = Common.return_response(False, status.HTTP_304_NOT_MODIFIED, 
                                                 'Players Excced 15')
            return Response(response, status.HTTP_304_NOT_MODIFIED)
        players = TPS_Users.objects.all()
        serializers = TPSUserResponseSerializer(players, many=True)

    response = Common.return_response(True, status.HTTP_200_OK, 
                                                 'Team Details Fetched', serializers.data)
    return Response(response, status = status.HTTP_200_OK) 
    
@api_view(['PATCH'])
@permission_classes(And(IsAuthenticated, IsCapitan))
def remove_team_players(request):
    captain_id  = request.data['idPlayers']
    team_members = request.data['team_members']
    team_id = Common.get_team_id(captain_id)
    team = Teams.object.get(idTeams = team_id)
    for member in team_members:
        player = TPS_Users.objects.get(idPlayers = member)
        player.idTeams = 1
        team.teams_players = team.teams_players.replace(member,'')
        team.teams_players = team.teams_players.replace(',,',',')
        serializers = TPSUserResponseSerializer(player)
        if serializers.is_valid():
            serializers.save()
            team.save()
    players = TPS_Users.objects.all()
    serializers = TPSUserResponseSerializer(players, many=True)

    response = Common.return_response(True, status.HTTP_200_OK, 
                                     'Team Details Fetched', serializers.data)
    return Response(response, status = status.HTTP_200_OK) 

@api_view(['PATCH'])
@permission_classes(And(IsAuthenticated, IsAdmin))
def approve_team(request):
    team_id  = request.data['idTeams']
    team = Teams.objects.get(idTeams = team_id)
    team_serializer = TeamsSerializer(team)
    team_members = team_serializer.data.team_members
    if len(team_members.split(',')) < 15:
        team_serializer.is_approved = True
        team_serializer.save()
        response = Common.return_response(True, status.HTTP_200_OK, 
                                     'Team Details Fetched', team_serializer.data)
        return Response(response, status = status.HTTP_200_OK)
    else:
        response = Common.return_response(False, status.HTTP_304_NOT_MODIFIED, 
                                                 'Players Excced 15')
        return Response(response, status.HTTP_304_NOT_MODIFIED)

        


