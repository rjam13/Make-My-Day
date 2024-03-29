# Generated by Django 4.0.5 on 2022-07-21 18:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_celery_beat', '0016_alter_crontabschedule_timezone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.BigAutoField(db_column='course_id', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('access_code', models.CharField(blank=True, default='', max_length=100)),
                ('year', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1900), main.models.max_value_current_year])),
                ('semester', models.CharField(choices=[('SPRING', 'Spring'), ('SUMMER', 'Summer'), ('FALL', 'Fall')], default='SUMMER', max_length=120)),
            ],
        ),
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
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_to_send', models.TimeField(null=True)),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('schedule', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.crontabschedule')),
                ('student', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('instructor_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor', to='main.instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='students', through='main.Notification', to='main.student'),
        ),
    ]
