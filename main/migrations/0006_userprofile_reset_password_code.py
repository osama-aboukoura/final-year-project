# Generated by Django 2.1.2 on 2019-01-24 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_userprofile_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='reset_password_code',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
