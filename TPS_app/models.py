from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class Teams(models.Model):
    teams_name = models.CharField(max_length = 50, unique = True)
    teams_sponsor = models.CharField(max_length = 20)
    team_capitan = models.CharField(max_length = 20, unique = True, default='')
    teams_players = models.CharField(max_length = 50, default='', blank=True)
    is_approved = models.BooleanField('Is Approved', default = False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teams_name

    class Meta:
        unique_together = ["teams_name", "teams_sponsor"]
        db_table = 'Teams'

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class TPS_Users(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length = 50)
    contactNo = models.CharField(max_length = 20)
    teams_name = models.CharField(max_length = 20, default = " ")
    is_capitan = models.BooleanField(default=False, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'TPS_Users'

    def __str__(self):
        return self.email

class Locations(models.Model):
    idLocations = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length = 50)
    location_city = models.CharField(max_length = 20)
    isBooked =  models.BooleanField('Is Booked', default = False)
    booking_date = models.DateTimeField(default = timezone.now)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location_name

    class Meta:
        db_table = 'Locations'

class Schedules(models.Model):
    idSchedule = models.AutoField(primary_key=True)
    teams1_name = models.CharField(max_length = 100, default='')
    teams2_name = models.CharField(max_length = 100, default='')
    match_date = models.TextField(max_length = 20, default='')
    idLocations = models.IntegerField()
    result = models.IntegerField(default = 0)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.idSchedule

    class Meta:
        db_table = 'Schedules'

# class TPS_Users(AbstractUser):
#     idPlayers = models.AutoField(primary_key=True)
#     username =  models.CharField(max_length = 50, unique=True)
#     password  = models.CharField(max_length=50)
#     Name = models.CharField(max_length = 50)
#     email =  models.EmailField(_('email address'), unique=True)
#     ContactNo = models.CharField(max_length = 20)
#     # idTeams = models.ForeignKey(Teams, default = 1, on_delete=models.CASCADE)
#     idTeams = models.CharField(max_length = 20)
#     is_admin = models.BooleanField(default=False, blank=True, null=True)
#     is_capitan = models.BooleanField(default=False, blank=True, null=True)
#     is_active = models.BooleanField('Is Active', default=False)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         db_table = 'TPS_Users'

#     def get_check_admin(self):
#         if self.is_admin:
#             return True