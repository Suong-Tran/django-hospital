# Generated by Django 4.0.3 on 2022-04-06 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_userprofile_physician_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_patient',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_physician',
            field=models.BooleanField(default=True),
        ),
    ]
