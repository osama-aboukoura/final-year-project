# Generated by Django 2.1.2 on 2019-02-12 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numOfPostsCommentsReplies', models.IntegerField(default=0)),
                ('numberOfLikes', models.IntegerField(default=0)),
                ('activationCode', models.CharField(blank=True, max_length=30)),
                ('resetPasswordCode', models.CharField(blank=True, max_length=30)),
                ('dateJoined', models.DateTimeField(auto_now_add=True)),
                ('profilePicture', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
