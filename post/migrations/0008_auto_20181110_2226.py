# Generated by Django 2.1.2 on 2018-11-10 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20181110_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentImage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='postImage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]