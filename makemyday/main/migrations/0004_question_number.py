# Generated by Django 4.0.4 on 2022-05-25 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_ans_answer_text_rename_ques_question_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
