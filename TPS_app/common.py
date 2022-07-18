import string, random

from TPS_app.models import Teams, TPS_Users, Locations, Schedules
from TPS_app.serializers import TPSUserResponseSerializer

class Common:
    def __init__(self) -> None:
        pass

    def generate_random_password(self):
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        length = 8
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        return "Terras_{0}".format("".join(password))

    def get_team_name(self, player_mail):
        player = TPS_Users.objects.get(email = player_mail)
        serializers = TPSUserResponseSerializer(player)
        return serializers.data['teams_name']

    def check_capitan(self, player_id):
        player_count = TPS_Users.objects.filter(Q(idPlayers = player_id) & Q(Players_Role = 2)).count()
        if player_count > 0:
            return True
        else:
            return False
    
    def get_player_id(self, username):
        player = TPS_Users.objects.filter(email=username).values('idPlayers')[0]
        return player

    def return_response(self, success, statusCode, message, data=''):
        response = {}
        response['success'] = success
        response['statusCode'] = statusCode
        response['message'] = message
        response['data'] = data
        return response