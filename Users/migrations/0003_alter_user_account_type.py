# Generated by Django 5.1.6 on 2025-03-10 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_user_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('patient', 'Patient'), ('companion', 'Companion')], default='Companion', max_length=20),
        ),
    ]
