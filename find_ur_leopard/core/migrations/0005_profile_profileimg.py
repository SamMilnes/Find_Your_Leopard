# Generated by Django 4.1.4 on 2022-12-09 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_profile_location_alter_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
    ]
