# Generated by Django 4.0.1 on 2022-01-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signup_holiday',
            field=models.CharField(max_length=200, null=True),
        ),
    ]