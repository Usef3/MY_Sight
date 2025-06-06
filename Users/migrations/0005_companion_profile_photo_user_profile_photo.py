# Generated by Django 5.1.6 on 2025-04-30 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_companion_user_alter_patient_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companion',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='companion_photos/'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
