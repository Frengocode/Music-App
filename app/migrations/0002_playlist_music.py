# Generated by Django 5.0.4 on 2024-04-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='music',
            field=models.FileField(default=1, upload_to='musics/'),
            preserve_default=False,
        ),
    ]
