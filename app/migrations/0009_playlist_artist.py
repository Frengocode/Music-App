# Generated by Django 5.0.4 on 2024-04-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_customuser_prime_plus'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='artist',
            field=models.CharField(default=1, max_length=50, verbose_name='The Singer'),
            preserve_default=False,
        ),
    ]
