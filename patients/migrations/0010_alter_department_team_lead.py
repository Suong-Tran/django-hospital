# Generated by Django 4.0.3 on 2022-04-09 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0009_department_team_lead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='team_lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.userprofile'),
        ),
    ]
