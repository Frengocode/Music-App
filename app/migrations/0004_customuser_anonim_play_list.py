# Generated by Django 5.0.4 on 2024-04-28 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_commentmodel_music_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='anonim_play_list',
            field=models.BooleanField(default=False),
        ),
    ]