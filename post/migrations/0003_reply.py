# Generated by Django 2.1.2 on 2018-11-03 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20181103_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replyContent', models.TextField()),
                ('replyBy', models.CharField(max_length=30)),
                ('replyDate', models.DateTimeField()),
                ('replyNumberOfLikes', models.IntegerField()),
                ('replyNumberOfVotes', models.IntegerField()),
                ('replyNumberOfFlags', models.IntegerField()),
                ('replytoComment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Comment')),
            ],
        ),
    ]
