# Generated by Django 4.2.6 on 2023-11-01 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0006_alter_user_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile-pictures/user-default.png', null=True, upload_to='shams-media/profile-pictures/', verbose_name='Profil rasmi'),
        ),
    ]