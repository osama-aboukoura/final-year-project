# Generated by Django 2.1.2 on 2018-11-26 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0026_auto_20181124_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postFlags',
            field=models.ManyToManyField(blank=True, related_name='post_flags', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postLikes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postVotersDown',
            field=models.ManyToManyField(blank=True, related_name='post_votes_down', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postVotersUp',
            field=models.ManyToManyField(blank=True, related_name='post_votes_up', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile'),
        ),
    ]
