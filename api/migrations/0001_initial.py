# Generated by Django 4.2.3 on 2023-08-19 03:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_name', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('nick_name', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=100)),
                ('img', models.ImageField(blank=True, null=True, upload_to='user_img')),
                ('role', models.CharField(choices=[('helper', 'helper'), ('helped', 'helped')], default='helper', max_length=10)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('review', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('public_service', 'public_service'), ('phone', 'phone'), ('computer', 'computer'), ('print', 'print')], max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('voice_file', models.FileField(blank=True, null=True, upload_to='voice_file')),
                ('context', models.TextField()),
                ('helper_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('helped_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('status', models.CharField(choices=[('wait', 'wait'), ('proceed', 'proceed'), ('success', 'success')], default='wait', max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
