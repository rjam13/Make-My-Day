# Generated by Django 4.0.4 on 2022-06-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_alter_activated_question_bank_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_bank',
            name='time_Limit',
            field=models.IntegerField(default=60, help_text='duration of each question in minutes'),
        ),
    ]
