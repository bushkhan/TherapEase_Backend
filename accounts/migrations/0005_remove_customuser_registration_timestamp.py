# Generated by Django 4.2.6 on 2023-10-18 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_customuser_registration_timestamp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="registration_timestamp",
        ),
    ]