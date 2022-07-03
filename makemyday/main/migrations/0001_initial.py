# Generated by Django 4.0.5 on 2022-07-03 22:02

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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(default='', max_length=255, unique=True)),
                ('student_id', models.CharField(blank=True, max_length=255)),
                ('instructor_id', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('instructor_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.BigAutoField(db_column='course_id', primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('instructors', models.ManyToManyField(related_name='instructors', to='main.instructor')),
                ('students', models.ManyToManyField(related_name='students', to='main.student')),
            ],
        ),
    ]
