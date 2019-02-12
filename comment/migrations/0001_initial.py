# Generated by Django 2.1.2 on 2019-02-12 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentContent', models.TextField(verbose_name='Comment on Post:')),
                ('commentImage', models.ImageField(blank=True, null=True, upload_to='')),
                ('commentDate', models.DateTimeField(auto_now_add=True)),
                ('commentNumberOfVotes', models.IntegerField(default=0)),
                ('commentDisabled', models.BooleanField(default=False)),
                ('commentAccepted', models.BooleanField(default=False)),
                ('commentBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile')),
                ('commentFlags', models.ManyToManyField(blank=True, related_name='comment_flags', to='main.UserProfile')),
                ('commentLikes', models.ManyToManyField(blank=True, related_name='comment_likes', to='main.UserProfile')),
                ('commentOnPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post')),
                ('commentVotersDown', models.ManyToManyField(blank=True, related_name='comment_votes_down', to='main.UserProfile')),
                ('commentVotersUp', models.ManyToManyField(blank=True, related_name='comment_votes_up', to='main.UserProfile')),
            ],
            options={
                'ordering': ['-commentNumberOfVotes'],
            },
        ),
    ]
