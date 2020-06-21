# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, spotify_user_id, spotify_username, access_token, refresh_token, playlist_time, last_login):
        user = self.model(
            spotify_user_id=spotify_user_id,
            spotify_username=spotify_username,
            access_token=access_token,
            refresh_token=refresh_token,
            playlist_time=playlist_time,
            last_login=timezone.now()
        )
        user.save(using=self._db)
        return user


class CustomUser(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    spotify_user_id = models.CharField(unique=True, max_length=255)
    spotify_username = models.CharField(unique=True, max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    playlist_time = models.TimeField(blank=True, null=True)
    last_login = models.DateTimeField()
    objects = CustomUserManager()
    USERNAME_FIELD = 'spotify_username'
    REQUIRED_FIELDS = []

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_user_id(self):
        return self.user_id

    def get_spotify_user_id(self):
        return self.spotify_user_id

    def get_spotify_username(self):
        return self.spotify_username

    def get_access_token(self):
        return self.access_token

    def get_refresh_token(self):
        return self.refresh_token

    def get_playlist_time(self):
        return self.playlist_time

    def get_last_login(self):
        return self.last_login

    class Meta:
        managed = False
        db_table = 'users'


class Job(models.Model):
    user = models.OneToOneField('CustomUser', models.CASCADE, primary_key=True)
    time = models.TimeField()

    def get_user_id(self):
        return self.user_id

    def get_time(self):
        return self.time

    class Meta:
        managed = False
        db_table = 'jobs'

