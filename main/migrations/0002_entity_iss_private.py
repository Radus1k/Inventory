# Generated by Django 4.2.1 on 2023-06-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='iss_private',
            field=models.BooleanField(default=True),
        ),
    ]
