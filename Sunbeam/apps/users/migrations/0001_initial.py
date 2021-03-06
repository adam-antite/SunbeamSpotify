# Generated by Django 3.0.7 on 2020-06-21 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('spotify_user_id', models.CharField(max_length=255, unique=True)),
                ('spotify_username', models.CharField(max_length=255, unique=True)),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('playlist_time', models.TimeField(blank=True, null=True)),
                ('last_login', models.DateTimeField()),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('time', models.TimeField()),
            ],
            options={
                'db_table': 'jobs',
                'managed': False,
            },
        ),
    ]
