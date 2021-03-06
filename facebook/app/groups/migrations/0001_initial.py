# Generated by Django 3.2.5 on 2021-09-27 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the was las modified.', verbose_name='modified at')),
                ('name', models.CharField(help_text='group name', max_length=130)),
                ('slug_name', models.SlugField(help_text='slug name', max_length=60, unique=True)),
                ('about', models.CharField(blank=True, help_text='group description', max_length=200)),
                ('cover_photo', models.ImageField(blank=True, help_text='group picture', null=True, upload_to='groups/pictures/')),
                ('is_public', models.BooleanField(default=True, help_text='Public groups can be found by other users')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the was las modified.', verbose_name='modified at')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the was las modified.', verbose_name='modified at')),
                ('is_admin', models.BooleanField(default=False, help_text='Group admin can have action on a group.')),
                ('is_active', models.BooleanField(default=False, help_text='Only active users are allowed to interact in the group.')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
