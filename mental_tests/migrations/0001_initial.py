# Generated by Django 4.1.6 on 2023-10-19 16:39

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
            name="AnxietyTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_1", models.IntegerField()),
                ("question_2", models.IntegerField()),
                ("question_3", models.IntegerField()),
                ("question_4", models.IntegerField()),
                ("question_5", models.IntegerField()),
                ("question_6", models.IntegerField()),
                ("question_7", models.IntegerField()),
                ("total", models.IntegerField()),
                ("result", models.CharField(max_length=255)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
