import requests

from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from TPS_app.models import Teams, Players, Locations, Schedules
from TPS_app.serializers import TeamsSerializer, PlayersSerializer
from TPS_app.serializers import LocationsSerializer, SchedulesSerializer

# Create your views here.
@api_view(['GET', 'POST','PUT','PATCH','DELETE'])
def teams_view(request):
    if request.method == 'GET':
        if 'idTeams' in request.data.keys():
            try:
                team = Teams.objects.get(idTeams = request.data['idTeams'])
                serializers = TeamsSerializer(team)
                return Response(serializers.data, status = status.HTTP_200_OK)
            except Teams.DoesNotExist:
                return Response({'msg':'No Teams Found', 'staus':status.HTTP_404_NOT_FOUND})
        else:
            teams = Teams.objects.all()
            serializers = TeamsSerializer(teams, many=True)
            return Response(serializers.data)
    elif request.method == 'POST':
        serializers = TeamsSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        print(request.data)
        try:
            team = Teams.objects.get(idTeams = request.data['idTeams'])
        except Teams.DoesNotExist:
            return Response({'msg':'No Teams Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = TeamsSerializer(team, request.data)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            return Response(serializers.data,  status = status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        print(request.data)
        try:
            team = Teams.objects.get(idTeams = request.data['idTeams'])
        except Teams.DoesNotExist:
            return Response({'msg':'No Teams Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = TeamsSerializer(team, request.data, partial=True)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            return Response(serializers.data,  status = status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if 'idTeams' in request.data.keys():
            Teams.objects.filter(śidTeams = request.data['idTeams']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg':'Specify Teams ID','staus':status.HTTP_400_BAD_REQUEST})

@api_view(['GET', 'POST','PUT','PATCH','DELETE'])
def players_view(request):
    if request.method == 'GET':
        if 'idPlayers' in request.data.keys():
            try:
                player = Players.objects.get(idPlayers = request.data['idPlayers'])
                serializers = PlayersSerializer(player)
                return Response(serializers.data, status = status.HTTP_200_OK)
            except Players.DoesNotExist:
                return Response({'msg':'No Players Found', 'staus':status.HTTP_404_NOT_FOUND})
        else:
            players = Players.objects.all()
            serializers = PlayersSerializer(players, many=True)
            return Response(serializers.data)
    elif request.method == 'POST':
        serializers = PlayersSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        print(request.data)
        try:
            player = Players.objects.get(idPlayers = request.data['idPlayers'])
        except Players.DoesNotExist:
            return Response({'msg':'No Players Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = PlayersSerializer(player, request.data, partial=True)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            return Response(serializers.data,  status = status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        print(request.data)
        try:
            player = Players.objects.get(idPlayers = request.data['idPlayers'])
        except Players.DoesNotExist:
            return Response({'msg':'No Players Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = PlayersSerializer(player, request.data)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            return Response(serializers.data,  status = status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if 'idPlayers' in request.data.keys():
            Players.objects.filter(idPlayers = request.data['idPlayers']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg':'Specify Players ID','staus':status.HTTP_400_BAD_REQUEST})

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
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
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        print(request.data)
        try:
            location = Locations.objects.get(idLocations = request.data['idLocations'])
        except Locations.DoesNotExist:
            return Response({'msg':'No Locations Found', 'staus':status.HTTP_404_NOT_FOUND})
        serializers = LocationsSerializer(location, request.data, partial=True)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            return Response(serializers.data,  status = status.HTTP_200_OK)

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
            return Response(serializers.data,  status = status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if 'idLocations' in request.data.keys():
            Locations.objects.filter(idLocations = request.data['idLocations']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg':'Specify Locations ID','staus':status.HTTP_400_BAD_REQUEST})

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
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
            data = {
                'idLocations' : request.data['idLocations'],
                'Location_Booking' : 1
            }
            requests.patch('http://127.0.0.1:8000/TPS_app/locations/', data = data)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
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
            return Response(serializers.data,  status = status.HTTP_200_OK)
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

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if 'idSchedule' in request.data.keys():
            Schedules.objects.filter(idSchedule = request.data['idSchedule']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg':'Specify Schedules ID','staus':status.HTTP_400_BAD_REQUEST})

@api_view(['GET'])
def get_schedules(request):
    if 'idPlayers' in request.data.keys():
        print(request.data) 
        try:
            player = Players.objects.get(idPlayers = request.data['idPlayers'])
            print(type(player))
            serializers = PlayersSerializer(player)
            print("players", serializers.data['idTeams'])
            schedules = Schedules.objects.filter(
                Q(Teams1_ID=serializers.data['idTeams']) | Q(Teams2_ID=serializers.data['idTeams'])).values(
                    'idSchedule','Teams1_ID','Teams2_ID','Match_date','idLocations'
                )
            if len(schedules.values()) > 0:
                return Response(schedules.values(),  status = status.HTTP_200_OK) 
            else:
                return Response({'msg':'No Schedules Found', 'staus':status.HTTP_404_NOT_FOUND})
        except Players.DoesNotExist:
            return Response({'msg':'No Players Found', 'staus':status.HTTP_404_NOT_FOUND})    
    else:
        return Response({'msg':'Specify Players ID','staus':status.HTTP_400_BAD_REQUEST})

@api_view(['GET'])
def get_team_members(request):
    if 'idPlayers' in request.data.keys(): 
        try:
            player = Players.objects.get(idPlayers = request.data['idPlayers'])
            serializers = PlayersSerializer(player)
            team_players = Players.objects.filter(idTeams=serializers.data['idTeams']).values('idPlayers','Players_Name')
            if len(team_players.values()) > 0:
                return Response(team_players.values(),  status = status.HTTP_200_OK) 
            else:
                return Response({'msg':'No Teams players Found', 'staus':status.HTTP_404_NOT_FOUND})
            return Response(serializers.data,  status = status.HTTP_200_OK)
        except Players.DoesNotExist:
            return Response({'msg':'No Players Found', 'staus':status.HTTP_404_NOT_FOUND})
    else:
        return Response({'msg':'Specify Players ID','staus':status.HTTP_400_BAD_REQUEST})



