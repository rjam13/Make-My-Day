# Generated by Django 4.0.5 on 2022-07-11 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0016_alter_crontabschedule_timezone'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activated_question_bank',
            name='schedule',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.crontabschedule'),
        ),
    ]
