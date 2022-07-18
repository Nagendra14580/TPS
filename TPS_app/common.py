import string, random

from TPS_app.models import Teams, TPS_Users, Locations, Schedules

class Common:
    def __init__(self) -> None:
        pass

    def generate_random_password():
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        length = 8
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        return "Terras_".join(password)

    def get_team_id(player_id):
        print("Player id",player_id)
        player = Players.objects.get(idPlayers = player_id)
        serializers = PlayersSerializer(player)
        return serializers.data['idTeams']

    def check_capitan(player_id):
        player_count = Players.objects.filter(Q(idPlayers = player_id) & Q(Players_Role = 2)).count()
        if player_count > 0:
            return True
        else:
            return False
    
    def return_response(self, success, statusCode, message, data=''):
        response = {}
        response['success'] = success
        response['statusCode'] = statusCode
        response['message'] = message
        response['data'] = data
        return response