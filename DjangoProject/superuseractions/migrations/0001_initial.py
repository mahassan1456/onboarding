# Generated by Django 4.1.7 on 2023-03-16 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pproducts.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserHistoryTable",
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
                (
                    "action_time",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[("1", "Create"), ("2", "Update"), ("0", "Delete")],
                        max_length=1,
                    ),
                ),
                ("action_code", models.CharField(default="", max_length=16, null=True)),
                (
                    "action_verbose",
                    models.CharField(default="", max_length=128, null=True),
                ),
                ("change_type", models.CharField(default="", max_length=32, null=True)),
                ("action_obj", pproducts.fields.MyJsonField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
