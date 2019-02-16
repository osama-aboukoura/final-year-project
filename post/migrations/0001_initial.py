# Generated by Django 2.1.2 on 2019-02-16 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postTitle', models.CharField(max_length=80, verbose_name='Post Title')),
                ('postTopic', models.CharField(max_length=30, verbose_name='Post Topic')),
                ('postContent', models.TextField(verbose_name='Post')),
                ('postImage', models.ImageField(blank=True, null=True, upload_to='')),
                ('postLastUpdated', models.DateTimeField(auto_now=True)),
                ('postDate', models.DateTimeField(auto_now_add=True)),
                ('postNumberOfVotes', models.IntegerField(default=0)),
                ('postNumberOfComments', models.IntegerField(default=0)),
                ('postDisabled', models.BooleanField(default=False)),
                ('postClosed', models.BooleanField(default=False)),
                ('postFlags', models.ManyToManyField(blank=True, related_name='post_flags', to='main.UserProfile')),
                ('postLikes', models.ManyToManyField(blank=True, related_name='post_likes', to='main.UserProfile')),
                ('postVotersDown', models.ManyToManyField(blank=True, related_name='post_votes_down', to='main.UserProfile')),
                ('postVotersUp', models.ManyToManyField(blank=True, related_name='post_votes_up', to='main.UserProfile')),
                ('postedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile')),
            ],
            options={
                'ordering': ['-postNumberOfVotes', '-postDate'],
            },
        ),
    ]
