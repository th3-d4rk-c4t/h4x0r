# Generated by Django 5.0.6 on 2024-09-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='secret_question',
        ),
        migrations.AddField(
            model_name='member',
            name='answer',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='member',
            name='question',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
