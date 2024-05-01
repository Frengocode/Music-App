from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class MusicCategory(models.TextChoices):

    POP = 'Поп', 'Поп'
    ROCK = 'Рок', 'Рок'
    CLASSIC = 'Класические','Класические'
    FUTURE = 'Будущие', 'Будущие'

class PlayList(models.Model):

    albom = models.ImageField(upload_to='albom/')
    artist = models.CharField(max_length=50, verbose_name='The Singer')
    music_title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='love_btn', blank=True)
    category = models.CharField(max_length=50, choices=MusicCategory)
    music = models.FileField(upload_to='musics/')
    music_country = CountryField()
    prime_music = models.BooleanField(default=False)

    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Название Песни{self.music_title}'


class CustomUser(AbstractUser):

    profile_photo = models.ImageField(upload_to='profile_photo', blank=True)
    user_play_list = models.ManyToManyField(PlayList, related_name='user_lovely_playlists', blank=True)
    play_list = models.CharField(max_length=50, choices = MusicCategory , verbose_name='Что Вы Любите Слушать ')
    anonim_play_list = models.BooleanField(default=False)
    country = CountryField() 
    prime_plus = models.BooleanField(default=False)

class CommentModel(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    music = models.ForeignKey(PlayList, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=50, verbose_name='Комментария')

    class Meta:
        ordering = ['-created_at']


class GetPrimePluse(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField()
    face_photo = models.ImageField(upload_to='face_photo/')
    phone_number = models.CharField(max_length=50, verbose_name='phone number')

