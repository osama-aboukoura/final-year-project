# Generated by Django 2.1.2 on 2018-11-30 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userprofile_activation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='activation_code',
            field=models.CharField(max_length=30),
        ),
    ]