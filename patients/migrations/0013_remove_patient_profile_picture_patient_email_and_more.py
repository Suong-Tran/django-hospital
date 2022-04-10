# Generated by Django 4.0.3 on 2022-04-10 01:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0012_patient_date_added_patient_profile_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(default=9999999, max_length=20),
            preserve_default=False,
        ),
    ]