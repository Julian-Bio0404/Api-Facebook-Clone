# Generated by Django 3.2.5 on 2021-09-27 22:21

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
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the was las modified.', verbose_name='modified at')),
                ('message', models.CharField(help_text='notification message', max_length=200)),
                ('notification_type', models.CharField(choices=[('group invitation', 'Group Invitation'), ('page invitation', 'Page Invitation'), ('reaction post', 'Reaction Post'), ('post', 'Post'), ('comment post', 'Comment Post'), ('reaction comment', 'Reaction Comment'), ('mention', 'Mention'), ('friend request', 'Friend Request'), ('friend accept', 'Friend Accept')], max_length=16)),
                ('issuing_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('receiving_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiving_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
