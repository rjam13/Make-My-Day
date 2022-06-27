# Generated by Django 4.0.5 on 2022-06-24 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(related_name='instructors', to='main.instructor'),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='students', to='main.student'),
        ),
    ]
