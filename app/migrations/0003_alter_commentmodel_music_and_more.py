# Generated by Django 5.0.4 on 2024-04-26 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_playlist_music'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='music',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.playlist'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='profile_photo'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_play_list',
            field=models.ManyToManyField(blank=True, related_name='user_lovely_playlists', to='app.playlist'),
        ),
    ]
