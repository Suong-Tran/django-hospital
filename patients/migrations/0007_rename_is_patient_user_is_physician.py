# Generated by Django 4.0.3 on 2022-04-07 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_patient_team'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_patient',
            new_name='is_physician',
        ),
    ]